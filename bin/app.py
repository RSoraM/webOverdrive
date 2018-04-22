# coding=utf-8
import json
import re

from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Flask, request
from flask_cors import CORS

from lib import Time as woTime
from lib.db import get_db
from lib.WebOverdrive import WebOverdrive

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
        msg['message'] = 'OK: ' + str(msg_id)
    else:
        msg['data'] = 'POST Available.'
        msg_id = db.test.insert_one(msg).inserted_id
        msg['message'] = 'OK: ' + str(msg_id)

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
    if auth['status'] != 200:
        return dumps(auth)
    elif auth['data']['level'] > 2:
        auth['status'] = 500
        auth['message'] = 'Error: Insufficient permissions'
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
    if auth['status'] != 200:
        return dumps(auth)
    elif auth['data']['level'] > 1:
        auth['status'] = 500
        auth['message'] = 'Error: Insufficient permissions'
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
    if auth['status'] != 200:
        return dumps(auth)
    elif auth['data']['level'] > 1:
        auth['status'] = 500
        auth['message'] = 'Error: Insufficient permissions'
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


# Search Spider
# auth: level n/a
@application.route('/searchSpider', methods=['POST'])
def search_spider():
    # data is result list
    msg = {
        'status': 200,
        'message': 'OK.',
        'data': {
            'length': 0,
            'result': []
        }
    }

    # if search nothing return 3 spider
    search_meta = request.form['search']
    skip = request.form['skip']

    if not search_meta:
        length = db.spider.count()
        found = db.spider.find().limit(3).skip(int(skip)).sort('_id', -1)
        msg['message'] = 'OK: Finished query'
    else:
        search_meta = re.compile(search_meta, re.IGNORECASE)
        length = db.spider.find({
            "$or": [{
                'spider.name': search_meta
            }, {
                'spider.description': search_meta
            }]
        }).count(True)
        found = db.spider.find({
            "$or": [{
                'spider.name': search_meta
            }, {
                'spider.description': search_meta
            }]
        }).limit(3).skip(int(skip)).sort('_id', -1)
        msg['message'] = 'OK: Finished query'

    # append result to data
    msg['data']['length'] = length
    for item in found:
        msg['data']['result'].append({
            'id':
            str(item.get('_id')),
            'spider':
            item.get('spider'),
            'createdDate':
            woTime.object_id_to_date(item.get('_id')),
            'status':
            item.get('status')
        })

    # feed back
    return dumps(msg)


# get Spider Status
# auth: level n/a
@application.route('/getStatus', methods=['POST'])
def getStatus():
    # data is running? running : runable
    msg = {'status': 200, 'message': 'OK.', 'data': ''}

    spider_id = request.form['id']

    if not spider_id:
        msg['status'] = 500
        msg['message'] = 'Error: Lack spider id'
        return dumps(msg)

    found = db.spider.find_one({
        '_id': ObjectId(spider_id)
    }, {
        '_id': 0,
        'spider': 0
    })
    if not found:
        msg['status'] = 500
        msg['message'] = 'Error: Spider not found'
        return dumps(msg)

    msg['message'] = 'OK: Get Spider Status'
    msg['data'] = found['running']

    # feed back
    return dumps(msg)


# Crawl Data Add(run spider) Remove List Download
# TODO
# JS
# auth: level <= 3
@application.route('/crawlData', methods=['POST'])
def add_crawl_task():
    # None Data
    msg = {'status': 200, 'message': 'OK.', 'data': None}
    spider_id = request.form['id']

    # Auth
    auth = json.loads(token_auth())
    if auth['status'] != 200:
        return dumps(auth)
    elif auth['data']['level'] > 3:
        auth['status'] = 500
        auth['message'] = 'Error: Insufficient permissions'
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

    # Running?
    if found.get("running"):
        msg['status'] = 300
        msg['message'] = 'Warning: Spider is running'

    # Add spider in queue
    spider.add(found)

    msg['message'] = 'OK: Add Spider in queue'

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
    if auth['status'] != 200:
        return dumps(auth)
    elif auth['data']['level'] > 2:
        auth['status'] = 500
        auth['message'] = 'Error: Insufficient permissions'
        return dumps(auth)

    # form check
    if not file_id:
        msg['status'] = 300
        msg['message'] = 'Warning: Select a file'
        return dumps(msg)

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
        "raw_pages": 0,
        "spider_id": 0
    }).sort('_id', -1)

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
