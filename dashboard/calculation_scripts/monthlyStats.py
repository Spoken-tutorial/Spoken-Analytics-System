"""
This script calculates monthly stats.
It takes logs of this or previous month from 'DailyStats' and calculates

1. Total page views : number of times a page is viewed by the user.
2. Unique visits : it is counted if user visits the site for the first time or he/she revisit it after 30 minutes.
3. First time visits : it is counted if user visits the site for the first time.
4. Returning visits : it is counted if a previous user visits the site after 30 minutes.
5. Unique visitors : number of users who visited the site.

Then is saves them to 'MonthlyStats'.

The script runs everyday after 12:00 AM.
"""

import datetime
from dashboard.models import DailyStats, MonthlyStats
from pytz import timezone
from django.conf import settings

# Timezone object used to localize time in current timezone
tz = timezone(settings.TIME_ZONE)

yesterday = datetime.datetime.now() - datetime.timedelta(1) # Yesterdays datetime
one_month_ago = datetime.datetime.now() - datetime.timedelta(yesterday.day) # one month ago datetime

one_month_ago_min = datetime.datetime.combine(one_month_ago, datetime.time.min) # one month ago min datetime
yesterday_max = datetime.datetime.combine(yesterday, datetime.time.max) # Yesterdays max datetime

# Make datetimes timezone aware
one_month_ago_min = tz.localize(one_month_ago_min)
yesterday_max = tz.localize(yesterday_max)

previous_month_stats = DailyStats.objects.filter(date__range=(one_month_ago_min, yesterday_max)).order_by('-datetime') # Getting data of the date from log collection

# variables to store counts
page_views = 0
unique_visits = 0
first_time_visits = 0
returning_visits = 0
unique_visitors = 0

for stats in previous_month_stats:
    page_views += stats.page_views
    unique_visits += stats.unique_visits
    first_time_visits += stats.first_time_visits
    returning_visits += stats.returning_visits
    unique_visitors += stats.unique_visitors

# delete the stats if the stats of this month exist
MonthlyStats.objects.filter(month_of_year=yesterday.month).delete()

previous_month_stats = MonthlyStats() # MonthlyStats object

previous_month_stats.datetime = tz.localize(yesterday) # localize yesterdays datetime using tz object
previous_month_stats.month_of_year = yesterday.month # get month number of previous month
previous_month_stats.year = yesterday.year # get year of previous month 
previous_month_stats.page_views = page_views
previous_month_stats.unique_visits = unique_visits
previous_month_stats.first_time_visits = first_time_visits
previous_month_stats.returning_visits = returning_visits
previous_month_stats.unique_visitors = unique_visitors

previous_month_stats.save() # saving the calculations to database
