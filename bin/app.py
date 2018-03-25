# coding=utf-8
import json
import re
from bson.json_util import dumps
from bson.objectid import ObjectId

from flask import Flask, request
from flask_cors import CORS

# import spider.Spider as woSpider
from tools import Time as woTime
from tools.db import get_db
from wo.WebOverdrive import WebOverdrive

db = get_db()
spider = WebOverdrive()

application = Flask(__name__)
CORS(application)


@application.route('/', methods=['GET', 'POST'])
def available_test():
    msg = {'status': 200, 'message': 'OK.', 'data': ''}

    if request.method == 'GET':
        msg['data'] = 'GET Available.'
        msg_id = db.test.insert_one(msg).inserted_id
        msg['message'] = 'OK: ' + msg_id
    else:
        msg['data'] = 'POST Available.'
        msg_id = db.test.insert_one(msg).inserted_id
        msg['message'] = 'OK: ' + msg_id

    return dumps(msg)


# Token Level:
# Level Right
# 0     Everything
# 1     Spider +-   Data +-
# 2     Spider +    Data +-
# 3     Spider n/a  Data +
@application.route('/auth', methods=['POST'])
def token_auth():
    # data is token and level
    msg = {'status': 200, 'message': 'OK.', 'data': {}}

    # get data from form
    token = request.form['token']

    found = db.token.find_one({'token': token})
    if found:
        msg['message'] = 'OK: Good token, Level: %s' % found['level']
        msg['data'] = {'token': token, 'level': found['level']}
    else:
        msg['status'] = 500
        msg['message'] = 'Error: Bad token'
        msg['data'] = {'token': token, 'level': 4}

    return dumps(msg)


# Form Check will be used to Add or Edit Spider
@application.route('/formCheck', methods=['POST'])
def form_check():
    # data is the error
    msg = {'status': 200, 'message': 'OK: Legal spider info'}

    # get data from form
    spider = json.loads(request.form['spider'])

    msg['data'] = spider

    def isIllegal(dic):
        for name in dic.iterkeys():
            if not dic[name] and name not in ('description', 'next'):
                return True
            elif isinstance(dic[name], list):
                for item in dic[name]:
                    isIllegal(item)
        return False

    if isIllegal(spider):
        msg['status'] = 500
        msg['message'] = 'Error: Illegal value'

    return dumps(msg)


# Spider Add Remove Edit Search
# Add Spider
# auth: level <= 2
@application.route('/addSpider', methods=['POST'])
def add_spider():
    # data is spider's inserted id
    msg = {'status': 200, 'message': 'OK.', 'data': ''}
    spider = json.loads(request.form['spider'])

    # auth
    auth = json.loads(token_auth())
    if auth['status'] != 200 or auth['data']['level'] <= 2:
        return dumps(auth)

    # Legal?
    check = json.loads(form_check())
    if check['status'] != 200:
        return dumps(check)

    # Existed?
    found = db.spider.find({'spider.name': spider['name']})
    for item in found:
        if item['spider'] == spider:
            msg['status'] = 300
            msg['message'] = 'Warning: Exited Spider'
            return dumps(msg)

    # save to db
    spider_id = db.spider.insert_one({'spider': spider}).inserted_id

    # feed back
    msg['message'] = 'OK: Inserted spider'
    msg['data'] = str(spider_id)

    return dumps(msg)


# Delete Spider
# auth: level <= 1
@application.route('/rmSpider', methods=['POST'])
def rm_spider():
    # data is delete count
    msg = {'status': 200, 'message': 'OK.', 'data': 0}
    spider_id = request.form['id']

    # auth
    auth = json.loads(token_auth())
    if auth['status'] != 200 or auth['data']['level'] <= 1:
        return dumps(auth)

    found = db.spider.find_one_and_delete({'_id': ObjectId(spider_id)})

    if found:
        msg['message'] = 'OK: Delete spider from Database'
    else:
        msg['status'] = 500
        msg['message'] = 'Error: Find nothing on Database'

    return dumps(msg)


# Edit Spider
# auth: level <= 1
@application.route('/editSpider', methods=['POST'])
def edit_spider():
    # data is spider before updated
    msg = {'status': 200, 'message': 'OK.', 'data': {}}
    spider = json.loads(request.form['spider'])
    spider_id = request.form['id']

    # auth
    auth = json.loads(token_auth())
    if auth['status'] != 200 or auth['data']['level'] <= 1:
        return dumps(auth)

    # Legal?
    check = json.loads(form_check())
    if check['status'] != 200:
        return dumps(check)

    # Find and update
    result = db.spider.find_one_and_update({
        '_id': ObjectId(spider_id)
    }, {'$set': {
        'spider': spider
    }})

    # feed back
    if result:
        msg['message'] = 'OK: Updated spider'
        msg['data'] = result
    else:
        msg['status'] = 500
        msg['message'] = 'Error: Update failed'

    return dumps(msg)

# TODO
# Fuzzy search
# Search Spider
# auth: level n/a
@application.route('/searchSpider', methods=['POST'])
def search_spider():
    # data is result list
    msg = {'status': 200, 'message': 'OK.', 'data': []}

    # if search nothing return 3 spider
    search_meta = request.form['search']
    if not search_meta:
        found = db.spider.find().limit(3)
        msg['message'] = 'OK: Get 3 items'
    else:
        search_meta = re.compile(search_meta)
        found = db.spider.find({
            "$or": [{
                'spider.name': search_meta
            }, {
                'spider.description': search_meta
            }]
        })
        msg['message'] = 'OK: Finished query'

    # append result to data
    for item in found:
        msg['data'].append({
            'id': str(item['_id']),
            'spider': item['spider'],
            'createdDate': woTime.object_id_to_date(item['_id'])
        })

    # feed back
    return dumps(msg)


# Crawl Data Add(run spider) Remove List Download
# TODO
# JS, rawPage
# BUG
# Data stay
# Add Crawl Data(run spider)
# auth: level <= 3
@application.route('/crawlData', methods=['POST'])
def run_spider():
    # data is crawl data's id
    msg = {'status': 200, 'message': 'OK.', 'data': ''}
    spider_id = request.form['id']

    # Auth
    auth = json.loads(token_auth())
    if auth['status'] != 200 or auth['data']['level'] <= 3:
        return dumps(auth)

    # Form check
    if not spider_id:
        msg['status'] = 500,
        msg['message'] = 'Error: Lack spider id'
        return dumps(msg)

    # Existed?
    found = db.spider.find_one({"_id": ObjectId(spider_id)})
    if not found:
        msg['status'] = 500
        msg['message'] = 'Error: Spider not found'
        return dumps(msg)

    # Run spider
    data = []
    data = spider.run(found['spider'], datas=data)
    file_id = db.crawl_data.insert_one({
        'data': data,
        'spider_id': ObjectId(spider_id)
    }).inserted_id

    msg['message'] = 'OK: Finished crawl'
    msg['data'] = str(file_id)

    return dumps(msg)


# Delete Crawl Data
# auth: level <= 2
@application.route('/rmCrawlData', methods=['POST'])
def rm_crawl_data():
    # data is delete count
    msg = {'status': 200, 'message': 'OK.', 'data': 0}
    file_id = request.form['id']

    # auth
    auth = json.loads(token_auth())
    if auth['status'] != 200 or auth['data']['level'] <= 2:
        return dumps(auth)

    found = db.crawl_data.find_one_and_delete({'_id': ObjectId(file_id)})

    if found:
        msg['message'] = 'OK: Delete data from Database'
    else:
        msg['status'] = 500
        msg['message'] = 'Error: Find nothing on Database'

    return dumps(msg)


# List Crawl Datas
# auth: level n/a
@application.route('/listCrawlData', methods=['POST'])
def list_crawl_data():
    # data lists dicts about crawl data's {id: '', data: ''}
    msg = {'status': 200, 'message': 'OK.', 'data': []}
    spider_id = request.form['id']

    # Form check
    if not spider_id:
        msg['status'] = 500,
        msg['message'] = 'Error: Lack spider id'
        return dumps(msg)

    # Find Crawl Data with spider_id
    found = db.crawl_data.find({
        "spider_id": ObjectId(spider_id)
    }, {
        "data": 0,
        "spider_id": 0
    })

    for item in found:
        msg['data'].append({
            'id': str(item['_id']),
            'date': woTime.object_id_to_date(item['_id'])
        })

    msg['message'] = 'OK: Finished query'

    return dumps(msg)


# Download Crawl Data
# auth: level n/a
@application.route('/dlCrawlData', methods=['POST'])
def dl_crawl_data():
    # data is crawl data
    msg = {'status': 200, 'message': 'OK.', 'data': []}
    file_id = request.form['id']

    if not file_id:
        msg['status'] = 500
        msg['message'] = 'Error: Select a file, please'
        return dumps(msg)

    found = db.crawl_data.find_one({'_id': ObjectId(file_id)})

    if not found:
        msg['status'] = 500
        msg['message'] = 'Error: Not such data'
    else:
        msg['message'] = 'OK: Found data'
        msg['data'] = found['data']
    return dumps(msg)