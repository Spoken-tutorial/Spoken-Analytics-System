"""
This script calculates weekly stats.
It takes logs of this or previous week from 'DailyStats' and calculates

1. Total page views : number of times a page is viewed by the user.
2. Unique visits : it is counted if user visits the site for the first time or he/she revisit it after 30 minutes.
3. First time visits : it is counted if user visits the site for the first time.
4. Returning visits : it is counted if a previous user visits the site after 30 minutes.
5. Unique visitors : number of users who visited the site.

Then is saves them to 'WeeklyStats'.

The script runs everyday after 12:00 AM.
"""

import datetime
from dashboard.models import DailyStats, WeeklyStats
from pytz import timezone
from django.conf import settings

# Timezone object used to localize time in current timezone
tz = timezone(settings.TIME_ZONE)

yesterday = datetime.datetime.now() - datetime.timedelta(i) # Yesterdays datetime
seven_days_ago = yesterday - datetime.timedelta(yesterday.weekday()) # 7 days ago datetime

seven_days_ago_min = datetime.datetime.combine(seven_days_ago, datetime.time.min) # Seven days ago min datetime
yesterday_max = datetime.datetime.combine(yesterday, datetime.time.max) # Yesterdays max datetime

# Make datetimes timezone aware
seven_days_ago_min = tz.localize(seven_days_ago_min)
yesterday_max = tz.localize(yesterday_max)

# Getting data of the previous week from 'DailyStats'
previous_week_stats = DailyStats.objects.filter(datetime__range=(seven_days_ago_min, yesterday_max)).order_by('datetime') 

# variables to store counts
page_views = 0
unique_visits = 0
first_time_visits = 0
returning_visits = 0
unique_visitors = 0

for stats in previous_week_stats:
    page_views += stats.page_views
    unique_visits += stats.unique_visits
    first_time_visits += stats.first_time_visits
    returning_visits += stats.returning_visits
    unique_visitors += stats.unique_visitors

# delete the stats if the stats of this week exist
WeeklyStats.objects.filter(week_of_year=yesterday.isocalendar()[1]).delete()

previous_week_stats = WeeklyStats() # WeeklyStats object

previous_week_stats.datetime = tz.localize(yesterday) # localize yesterdays datetime using tz object
previous_week_stats.week_of_year = yesterday.isocalendar()[1] # get week number of previous week
previous_week_stats.year = yesterday.year # get year of previous week 
previous_week_stats.page_views = page_views
previous_week_stats.unique_visits = unique_visits
previous_week_stats.first_time_visits = first_time_visits
previous_week_stats.returning_visits = returning_visits
previous_week_stats.unique_visitors = unique_visitors

previous_week_stats.save() # saving the calculations to database
