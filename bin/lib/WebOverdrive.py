# coding=utf-8
import os
import time
from multiprocessing import Pool, Manager, Queue

import requests
from bs4 import BeautifulSoup
from bson.objectid import ObjectId

import Time as woTime
from db import get_db
from Setting import Setting

db = get_db()


class WebOverdrive(object):
    def __init__(self, workers=2):
        self._task_queue = Manager().Queue()
        pool = Pool(workers)
        for i in range(0, workers):
            pool.apply_async(worker, (self._task_queue, ))
            print "task %s inited" % i

    def add(self, spider, task_setting={}):
        db.spider.find_one_and_update({
            "_id": ObjectId(spider.get("_id"))
        }, {"$set": {
            "running": True
        }})

        self._task_queue.put({
            'spider': spider,
            'setting': Setting(task_setting)
        })


def worker(queue):
    print 'worker inited (%s)' % os.getpid()
    while True:
        task = queue.get()
        spider = task.get('spider')
        task_setting = task.get('setting')

        file_id = db.crawl_data.insert_one({
            "spider_id":
            ObjectId(spider.get("_id"))
        }).inserted_id

        run(spider.get("spider"), file_id, task_setting)

        db.spider.find_one_and_update({
            "_id": ObjectId(spider.get("_id"))
        }, {"$set": {
            "running": False
        }})


def run(spider, file_id, setting, read=[]):
    time.sleep(setting.getDelay())

    # download pages
    html = requests.get(spider["url"], headers=setting.getHeader())
    html.encoding = 'utf-8'
    soup = BeautifulSoup(html.text, "lxml")

    # url deduplication
    read.append(spider["url"])

    # save raw pages
    db.crawl_data.find_one_and_update({
        "_id": ObjectId(file_id)
    }, {'$push': {
        "raw_pages": soup.prettify()
    }})

    # guess running js

    # parse data
    temp = []
    for item in spider["items"]:
        locals()[item["name"]] = soup.select(item["selector"])
        for index, obj in enumerate(locals()[item["name"]]):
            try:
                if item['attr'] != 'text':
                    temp[index][item["name"]] = obj.attrs[item["attr"]]
                else:
                    temp[index][item["name"]] = obj.get_text()
            except IndexError:
                temp.append({})
                if item['attr'] != 'text':
                    temp[index][item["name"]] = obj.attrs[item["attr"]]
                else:
                    temp[index][item["name"]] = obj.get_text()

    # append data
    db.crawl_data.find_one_and_update({
        "_id": ObjectId(file_id)
    }, {"$addToSet": {
        "data": {
            "$each": temp
        }
    }})

    # Recursive
    if spider["next"] != '':
        seed = soup.select(spider["next"])
    else:
        return

    if seed:
        try:
            seed_url = seed[0].attrs["href"]
        except KeyError:
            seed_url = None
            return

        if seed_url in read:
            return

        spider["url"] = seed_url
        run(spider, file_id, setting, read)

    return


# delay
# get html
# add html to db
# get soup
# get data
# if seed:
#     recursive
# esle:
#     add data to db
