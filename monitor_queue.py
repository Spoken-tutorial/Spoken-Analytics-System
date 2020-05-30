
import redis
import json
import datetime
import os
import sys
import logging
import time

from django.conf import settings
from django.apps import apps
import django

from celery import Celery

from logs_api.tasks import dump_json_logs

# importing and configuring the spoken settings.py file
sys.path.append(settings.BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'analytics_system.settings')
django.setup()

# redis and mongo clients
from analytics_system import REDIS_CLIENT, MONGO_CLIENT 

# configure the pymongo client
db = MONGO_CLIENT.logs
website_logs = db.website_logs
website_logs_js = db.website_logs_js

task_queue = ''
if settings.USE_MIDDLEWARE_LOGS:
    task_queue = 'middleware_log'
else:
    task_queue = 'js_log'


# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(name)s] [%(asctime)s] %(levelname)s : %(message)s')
logger = logging.getLogger('monitor_queue')


"""
Continuosly monitor the redis 'tasks' queue length.
if reaches >= MONGO_BULK_INSERT_COUNT items, pop the 
leftmost MONGO_BULK_INSERT_COUNT items and save them 
in MongoDB. (the items at the left of the queue 
are the ones that have been in the queue the longest,
since the queue is a FIFO structure).
"""
def monitor_queue ():

    while (True):

        try:
           
            if REDIS_CLIENT.llen(task_queue) >= settings.MONGO_BULK_INSERT_COUNT:

                logs = REDIS_CLIENT.lrange(task_queue, 0, settings.MONGO_BULK_INSERT_COUNT - 1)
                
                # trim the queue to remove the leftmost 10000 logs
                # TODO: check if there's any opportunity for data loss, i.e.
                # if it's possible for the queue size to increase between when the function 
                # ltrim() is called, and when the queue is actually trimmed. The newest logs
                # may be lost in this case.
                REDIS_CLIENT.ltrim(task_queue, start=settings.MONGO_BULK_INSERT_COUNT, end=-1)

                for i in range(len(logs)):

                    # Extract json data into dict
                    my_json = logs[i].decode('utf8')
                    logs[i] = json.loads(my_json)
                    # print (logs[i])
                
                t0 = time.clock()

                if settings.SAVE_LOGS_WITH_CELERY:

                    dump_json_logs.delay(logs)
                    logger.info(f'{len(logs)} items successfully sent to Celery in {time.clock() - t0} seconds.')

                else:
            
                    # insert into MongoDB
                    # the ordered=False option ensures that all the logs are attempted for insert,
                    # even if one of the intermediate logs fails the insertion.
                    # convert datetime from str to datetime object
                    for i in range(len(logs)):
                        logs[i]['datetime'] = datetime.datetime.strptime(logs[i]['datetime'], '%Y-%m-%d %H:%M:%S.%f')

                    if settings.USE_MIDDLEWARE_LOGS:
                        website_logs.insert_many([logs[i] for i in range(len(logs))], ordered=False)
                    else:
                        website_logs_js.insert_many([logs[i] for i in range(len(logs))], ordered=False)

                    logger.info(f'{len(logs)} items successfully inserted into MongoDB in {time.clock() - t0} seconds.')


            logger.info(f'Number of items in queue {task_queue}: {REDIS_CLIENT.llen(task_queue)}')
            time.sleep(settings.MONITOR_QUEUE_ITERATION_DELAY)
        except Exception:
            logger.exception("Exception occurred") 


if __name__ == '__main__':
    monitor_queue()  # This program can never crash once the monitor_queue() function is called.
