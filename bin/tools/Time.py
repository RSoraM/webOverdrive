import arrow
from bson.objectid import ObjectId


def object_id_to_date(object_id, tz='Asia/Shanghai'):
    if type(object_id) == str:
        return arrow.get(ObjectId(object_id).generation_time).to(tz).format()
    else:
        return arrow.get(object_id.generation_time).to(tz).format()


def now():
    return arrow.now()
