"""
This file can generate fake data for database.
change num_rows to desired number of rows to be inserted.
excute this file in python shell.
>> exec(open("gen_fake_data.py").read())
"""

import datetime
from dateutil import tz
import random
from django_populate import Faker
from dashboard.models import Log
import dateutil.parser

num_rows = 500000 # number of rows to insert

india_tz = tz.gettz('Asia/Kolkata')

# Creating populator object
populator = Faker.getPopulator()

event_names = ["event.video.watch", "event.cdcontent.download", "event.tutorial.search", "event.news", "event.login", "event.logout", "event.register", "event.software.training", "event.software.training.planner", "event.software.training.student.batch", "event.software.training.select.participants", "event.software.training.resource.center", "event.participant.login", "event.statistics", "event.statistics.training", "event.statistics.fdp.training", "event.statistics.tutorial.content", "event.statistics.online.test", "event.statistics.academic.center", "event.home.view"]
paths = ["/watch/", "/cdcontent/", "/tutorial-search/", "/news/", "/accounts/login/", "/accounts/logout/", "/accounts/register/", "/software-training/", "/software-training/training-planner/", "/software-training/student-batch/", "/software-training/select-participants/", "/software-training/resource-center/", "/participant/login/", "/statistics/", "/statistics/training/", "/statistics/pmmmnmtt/fdp/", "/statistics/tutorial-content/", "/statistics/online-test/", "/statistics/academic-center/", "home"]

def randomData():
    # path_info = lambda x: populator.generator.uri_path(deep=None)
    visited_by = lambda x: populator.generator.user_name()
    method = lambda x: random.choice(["GET", "POST"])
    city = lambda x: populator.generator.city()
    region = lambda x: populator.generator.state()
    country = lambda x: populator.generator.country()
    ip_address = lambda x: "127.0." + str(random.randint(0, 255)) + "." + str(random.randint(0, 255))
    event_name = lambda x: random.choice(event_names)
    path_info = lambda x: random.choice(paths)
    data = {
        'path_info': path_info,
        'visited_by': visited_by,
        'browser_info' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'request_data' : '{data: request_data}',
        'method': method,
        'event_name': event_name,
        'city': city,
        'region': region,
        'country': country,
        'ip_address':  ip_address,
        'datetime': lambda x: populator.generator.date_time_between(start_date='-4y', end_date='+18d', tzinfo=india_tz),
        'first_time_visit': lambda x: random.choice(["True", "False"]),
    }
    return data

# Adding data to populator object
populator.addEntity(Log, num_rows, randomData())

# Inserting data to database
populator.execute()