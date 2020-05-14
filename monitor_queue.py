
import redis
import json
import datetime
import os
from pymongo import MongoClient
from django.apps import apps

# importing the required module 
import time


# configurations for redis
r = redis.Redis(
    host='localhost',
    port=6379,
    db=0
)

# create and configure the pymongo client
client = MongoClient()
db = client.logs_api
logs_api = db.logs_api

while (True):

    if r.llen('tasks3') >= 5:

        try:

            logs = r.lrange('tasks3', 0, 4)
            # r.ltrim('tasks', start=1000)

            for i in range(len(logs)):
                r.lpop('tasks3')

                # Extract json data into dict
                my_json = logs[i].decode('utf8')
                logs[i] = json.loads(my_json)
                # print (logs[i])
            
            t0 = time.clock()

            for i in range (len(logs)):
                logs[i]['datetime'] = datetime.datetime.strptime(logs[i]['datetime'], '%Y-%m-%d %H:%M:%S.%f')
        
            logs_api.insert_many([logs[i] for i in range(len(logs))])

            t1 = time.clock() - t0

            print("Time elapsed: ", t1) # CPU seconds elapsed (floating point)

        except Exception as e:
            print (e)
