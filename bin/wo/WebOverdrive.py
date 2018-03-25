import requests
from bs4 import BeautifulSoup
import time

from Setting import Setting


class WebOverdrive(object):
    queue = []
    setting = Setting()

    def __init__(self, Setting=setting):
        return

    def add(self, spider):
        self.queue.append(spider)

    def run(self, spider, datas=[]):
        time.sleep(self.setting.getDelay())

        # download pages
        html = requests.get(spider["url"], headers=self.setting.getHeader())
        html.encoding = 'utf-8'
        soup = BeautifulSoup(html.text, "lxml")

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
        datas += temp

        # seed callback
        if spider["next"] != '':
            seed = soup.select(spider["next"])
            if seed:
                try:
                    seed_url = seed[0].attrs["href"]
                except KeyError:
                    seed_url = None
                else:
                    spider["url"] = seed_url
                    self.run(spider, datas)

        return datas