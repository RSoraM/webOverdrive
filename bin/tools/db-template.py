import urllib
from pymongo import MongoClient

DATA_URL = 'data/'
DB_USER = urllib.quote_plus('username')
DB_PWD = urllib.quote_plus('password')
DB_DOMAIN = urllib.quote_plus('domain.com')
DB_PORT = 27018
client = MongoClient('mongodb://%s:%s@%s:%s/' % (DB_DOMAIN, DB_PORT,DB_USER, DB_PWD))
db = client.webOverdrive


def get_db():
    return db
