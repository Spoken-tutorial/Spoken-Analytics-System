from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)


import redis
# Initialize redis client
REDIS_CLIENT = redis.Redis(
    host='localhost',
    port=6379,
    db=0
)

# Create and configure the pymongo client
from pymongo import MongoClient

MONGO_CLIENT = MongoClient()

import django
django.setup()
