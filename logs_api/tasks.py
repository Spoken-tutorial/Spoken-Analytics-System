# Create your Celery tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
import datetime

from django.conf import settings

# mongo client
from analytics_system import MONGO_CLIENT

# configurations for pymongo
db = MONGO_CLIENT.logs
website_logs_middleware = db.website_logs_middleware
website_logs_js = db.website_logs_js


# using bind=True on the shared_task decorator to turn the below function
# into a method of Task class. This lets us use self.retry for retrying
# failed tasks. Currently we are not retrying failed tasks.
@shared_task(bind=True)
def dump_json_logs(self, logs):  # celery task for bulk insertion of logs into MongoDB.

    # store in MongoDB
    try:

        # convert datetime from str to datetime object
        for i in range(len(logs)):
            logs[i]['datetime'] = datetime.datetime.strptime(logs[i]['datetime'], '%Y-%m-%d %H:%M:%S.%f')

        # insert into MongoDB
        # the ordered=False option ensures that all the logs are attempted for insert,
        # even if one of the intermediate logs fails the insertion.
        if settings.USE_MIDDLEWARE_LOGS:
            website_logs_middleware.insert_many([logs[i] for i in range(len(logs))], ordered=False)
        else:
            website_logs_js.insert_many([logs[i] for i in range(len(logs))], ordered=False)

    except Exception as e:  # catching a generic exception

        """
        Sending the task back into the queue with exponential
        backoff. If the task fails more than max_retries + 1 times,
        an error is display in the celery worker.
        """
        # self.retry(exc=exc, countdown=2 ** self.request.retries)

        with open("celery_errors_log.txt", "a") as f:
            f.write(str(e) + "\n")
