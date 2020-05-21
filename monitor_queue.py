
import redis
import json
import datetime
import os
import sys

import time

from django.conf import settings
from django.apps import apps
import django

from celery import Celery

from logs_api.tasks import dump_json_logs

# importing and configuring the spoken settings.py file
sys.path.append("/home/krithik/Desktop/Git/Spoken-Analytics-System")  # path to the parent dir of DjangoTastypie
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'analytics_system.settings')
django.setup()

# redis and mongo clients
from analytics_system import REDIS_CLIENT, MONGO_CLIENT 

# configure the pymongo client
db = MONGO_CLIENT.logs_api
logs_api = db.logs_api


"""
Continuosly monitor the redis 'tasks' queue length.
if reaches >= 10000 items, pop the leftmost 10000 items
and save them in MongoDB. (the items at the left of the
queue are the ones that have been in the queue the longest,
since the queue is a FIFO structure).
"""
while (True):

    if REDIS_CLIENT.llen('tasks3') >= 5:

        try:

            logs = REDIS_CLIENT.lrange('tasks3', 0, 4)
            
            # trim the queue to remove the leftmost 10000 logs
            # TODO: check if there's any opportunity for data loss, i.e.
            # if it's possible for the queue size to increase between when the function 
            # ltrim() is called, and when the queue is actually trimmed. The newest logs
            # may be lost in this case.
            REDIS_CLIENT.ltrim('tasks3', start=10000, end=REDIS_CLIENT.llen('tasks3'))

            for i in range(len(logs)):

                # Extract json data into dict
                my_json = logs[i].decode('utf8')
                logs[i] = json.loads(my_json)
                # print (logs[i])
            
            t0 = time.clock()

            if settings.SAVE_LOGS_WITH_CELERY:

                dump_json_logs.delay(logs)

            else:
        
                # insert into MongoDB
                # the ordered=False option ensures that all the logs are attempted for insert,
                # even if one of the intermediate logs fails the insertion.
                logs_api.insert_many([logs[i] for i in range(len(logs))], ordered=False)

            t1 = time.clock() - t0

            print("Time elapsed: ", t1) # CPU seconds elapsed (floating point)

        except Exception as e:
            print (e)