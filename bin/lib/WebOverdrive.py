import time
from multiprocessing import Process, Queue

import requests
from bs4 import BeautifulSoup
from bson.objectid import ObjectId

import Time as woTime
from db import get_db
from Setting import Setting

db = get_db()
_task_queue = Queue()


class WebOverdrive(object):
    setting = Setting()

    def __init__(self, setting=None):
        if setting:
            self.setting = setting

        self.p = Process(target=self.worker, args=(_task_queue, ))
        self.p.daemon = True
        self.p.start()
        print "%s WebOverdrive: %s" % (woTime.now(), "Inited")

    def worker(self, queue):
        while True:
            print "%s WebOverdrive: Waiting" % woTime.now()
            spider = queue.get()

            print "%s WebOverdrive: %s" % (
                woTime.now(),
                "Run Spider <%s>" % spider.get("spider").get("name"))

            file_id = db.crawl_data.insert_one({
                "spider_id":
                ObjectId(spider.get("_id"))
            }).inserted_id

            self.run(spider.get("spider"), file_id)

            db.spider.find_one_and_update({
                "_id": ObjectId(spider.get("_id"))
            }, {"$set": {
                "running": False
            }})

    def add(self, spider):
        print "%s WebOverdrive: %s" % (
            woTime.now(),
            "Add Spider <%s> in queue" % spider.get("spider").get("name"))
        db.spider.find_one_and_update({
            "_id": ObjectId(spider.get("_id"))
        }, {"$set": {
            "running": True
        }})

        _task_queue.put(spider)

    def run(self, spider, file_id, read=[]):
        time.sleep(self.setting.getDelay())

        # download pages
        print "%s WebOverdrive: %s" % (woTime.now(),
                                       "Downloading <%s>" % spider.get("url"))
        html = requests.get(spider["url"], headers=self.setting.getHeader())
        html.encoding = 'utf-8'
        soup = BeautifulSoup(html.text, "lxml")

        # url deduplication
        read.append(spider["url"])

        # save raw pages
        print "%s WebOverdrive: %s" % (
            woTime.now(), "Save <%s> in Database" % spider.get("url"))
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
            self.run(spider, file_id, read)

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
