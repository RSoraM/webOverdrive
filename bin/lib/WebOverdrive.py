# coding=utf-8
import os
import time
from multiprocessing import Manager, Pool, Process, Queue

import requests
from bs4 import BeautifulSoup
from bson.objectid import ObjectId

import Time as woTime
from db import get_db
from Setting import Setting

db = get_db()


class WebOverdrive(object):
    def __init__(self, download_workers=4):
        self._task_queue = Manager().Queue()
        self._download_queue = Manager().Queue()
        self._parse_queue = Manager().Queue()
        self._finish_queue = Manager().Queue()

        pool = Pool(download_workers + 4)

        print "Init task worker"
        pool.apply_async(task_worker, ({
            "task_queue": self._task_queue,
            "download_queue": self._download_queue
        }, ))

        for i in range(0, download_workers):
            print "Init download worker%s" % i
            pool.apply_async(download_worker,
                             ({
                                 "download_queue": self._download_queue,
                                 "parse_queue": self._parse_queue
                             }, ))

        print "Init parse worker"
        pool.apply_async(parse_worker, ({
            "parse_queue": self._parse_queue,
            "finish_queue": self._finish_queue
        }, ))

        print "Init finish worker"
        pool.apply_async(finish_worker, (self._finish_queue, ))

    def add(self, spider, task_setting={}):
        update_spider_status(spider.get("_id"), "Waiting...")

        package = {
            "spider_id": spider.get("_id"),
            "spider": spider.get("spider"),
            "file_id": "",
            "setting": Setting(task_setting)
        }
        self._task_queue.put(package)

    # TODO
    def stop(self, spider_id):
        update_spider_status(spider_id, "Stopping...")
        pass


def task_worker(queues):
    print 'task_worker inited (%s)' % os.getpid()

    task_queue = queues.get("task_queue")
    download_queue = queues.get("download_queue")

    while True:
        package = task_queue.get()

        spider_id = package.get("spider_id")

        update_spider_status(spider_id, "Running...")

        file_id = db.crawl_data.insert_one({
            "spider_id": ObjectId(spider_id)
        }).inserted_id

        package["file_id"] = file_id
        download_queue.put(package)


def download_worker(queues):
    print "downloader inited (%s)" % os.getpid()

    download_queue = queues.get("download_queue")
    parse_queue = queues.get("parse_queue")

    while True:
        package = download_queue.get()

        spider = package.get("spider")
        file_id = package.get("file_id")
        setting = package.get("setting")

        read = []
        url = spider["url"]
        next = spider["next"]

        task_stop_flag = False

        while url:

            if task_stop_flag:
                break

            read.append(url)

            # download pages
            try:
                html = requests.get(url, headers=setting.getHeader())
                html.encoding = "utf-8"
            except:
                print 'download error %s' % url
                break

            # tell parser
            package["html"] = html.text
            package["url"] = url
            parse_queue.put(package)

            # save raw pages
            db.crawl_data.find_one_and_update({
                "_id": ObjectId(file_id)
            }, {"$push": {
                "raw_pages": html.text
            }})

            # try get next pages
            soup = BeautifulSoup(html.text, "lxml")
            if next:
                seed = soup.select(next)
                if seed:
                    try:
                        url = seed[0].attrs["href"]
                        if url not in read:
                            time.sleep(setting.getDelay())
                        else:
                            url = None
                    except KeyError:
                        url = None
                else:
                    url = None
            else:
                url = None

        # ending singal
        package["finish"] = True
        parse_queue.put(package)


def parse_worker(queues):
    print "parser inited (%s)" % os.getpid()

    parse_queue = queues.get("parse_queue")
    finish_queue = queues.get("finish_queue")

    while True:
        package = parse_queue.get()

        if package.get("finish"):
            finish_queue.put(package)
            continue

        spider = package.get("spider")
        file_id = package.get("file_id")
        html = package.get("html")
        soup = BeautifulSoup(html, "lxml")

        temp = []

        # TODO check bug
        for item in spider["items"]:
            locals()[item["name"]] = soup.select(item["selector"])
            for index, obj in enumerate(locals()[item["name"]]):
                try:
                    if item["attr"] != "text":
                        temp[index][item["name"]] = obj.attrs[item["attr"]]
                    else:
                        temp[index][item["name"]] = obj.get_text()
                except IndexError:
                    temp.append({})
                    if item["attr"] != "text":
                        temp[index][item["name"]] = obj.attrs[item["attr"]]
                    else:
                        temp[index][item["name"]] = obj.get_text()

        db.crawl_data.find_one_and_update({
            "_id": ObjectId(file_id)
        }, {"$addToSet": {
            "data": {
                "$each": temp
            }
        }})


def finish_worker(finish_queue):
    print "closer inited (%s)" % os.getpid()

    while True:
        package = finish_queue.get()

        spider_id = package.get("spider_id")
        update_spider_status(spider_id, "Runable")


def update_spider_status(id, status):
    db.spider.find_one_and_update({
        "_id": ObjectId(id)
    }, {"$set": {
        "status": status
    }})
