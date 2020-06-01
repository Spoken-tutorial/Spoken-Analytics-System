"""
This script calculates daily stats.
It takes logs of previous day from 'Log' and calculates

1. Total page views : number of times a page is viewed by the user.
2. Unique visits : it is counted if user visits the site for the first time or he/she revisit it after 30 minutes.
3. First time visits : it is counted if user visits the site for the first time.
4. Returning visits : it is counted if a previous user visits the site after 30 minutes.
5. Unique visitors : number of users who visited the site.

Then is saves them to 'DailyStats'.

The script runs each day after 12:00 AM.
"""

import datetime
from dashboard.models import Log, DailyStats
from pytz import timezone
from django.conf import settings

# Timezone object used to localize time in current timezone
tz = timezone(settings.TIME_ZONE)

# Yesterdays datetime
yesterday = datetime.datetime.now() - datetime.timedelta(1)

yesterday_min = datetime.datetime.combine(yesterday, datetime.time.min) # Yesterdays min datetime
yesterday_max = datetime.datetime.combine(yesterday, datetime.time.max) # Yesterdays max datetime

# Make datetimes timezone aware
yesterday_min = tz.localize(yesterday_min)
yesterday_max = tz.localize(yesterday_max)

# Getting logs of yesterday from 'Log'
yesterdays_logs = Log.objects.filter(datetime__range=(yesterday_min, yesterday_max)).order_by('datetime')

unique_visitors = [] # Stores unique ip addresses

# Finding all unique ip addresses
for log in yesterdays_logs:
    if log.ip_address not in unique_visitors:
        unique_visitors.append(log.ip_address)

# Variable to check whether ip occurs for the first time (used for finding number of first time visits)
first_time = 0

# Variables to store counts
unique_visits = 0
first_time_visit = 0
returning_visits = 0

# caculating stats according to ip addresses
for ip in unique_visitors:
    first_time = 0
    for log in yesterdays_logs:
        if ip == log.ip_address:
            # if ip is found for the first time
            if first_time == 0:
                first_time = 1
                first_time_visit += 1
                unique_visits += 1
            else:
                # if same ip occurs after 30 minutes
                if ((log.datetime - prev_datetime).seconds / 60) > 30:
                    returning_visits += 1
                    unique_visits += 1
            prev_datetime = log.datetime

daily_stats = DailyStats() # DailyStats object

daily_stats.datetime = tz.localize(yesterday) # localize yesterdays datetime using tz object
daily_stats.date = yesterday.date()
daily_stats.page_views = len(yesterdays_logs) # total page views will be equal to number of logs created on previous day
daily_stats.unique_visits = unique_visits
daily_stats.first_time_visits = first_time_visit
daily_stats.returning_visits = returning_visits
daily_stats.unique_visitors = len(unique_visitors) # number of unique visitor is equal to number of unique ip addresses

daily_stats.save() # saving the calculations to database