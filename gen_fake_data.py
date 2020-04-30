"""
This file can generate fake data for database.
Call this file in python shell to execute it.
>> source gen_fake_data.py
"""

import datetime
import random
from django_populate import Faker
from dashboard.models import Log
import dateutil.parser

populator = Faker.getPopulator()

def randomData():
    data = {
        'path_info': lambda x: populator.generator.uri_path(deep=None),
        'visited_by': lambda x: populator.generator.user_name(),
        'browser_info' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'request_data' : '{data: request_data}',
        'method': lambda x: random.choice(["GET", "POST", "PUT", "DELETE"]),
        'event_name': '',
        'city': lambda x: populator.generator.city(),
        'region': lambda x: populator.generator.state(),
        'country': lambda x: populator.generator.country(),
        'ip_address':  lambda x: populator.generator.ipv4(network=False, address_class=None, private=None),
        'timestamp': lambda x: populator.generator.date_time_between(start_date='-10y', end_date='now'),
        'view_args': 'view_args',
        'view_kwargs': 'view_kwargs'
    }
    return data

n = 10 # number of rows to inserted

populator.addEntity(Log, n, randomData())
populator.execute()