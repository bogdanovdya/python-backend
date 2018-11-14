import pymongo
import json
from datetime import datetime, date, time

mng_client = pymongo.MongoClient('localhost', 27017)
mng_db = mng_client['local']
db_cm = mng_db['my_collection']


def pagination(page_size, c_skip=0):
    if c_skip > 0:
        db_cm.find().skip(c_skip).limit(page_size)
        return pagination(page_size, (c_skip+page_size))
    else:
        db_cm.find().limit(page_size)
        return pagination(page_size, page_size)


if __name__ == '__main__':
    pagination(100)
