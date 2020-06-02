"""
This script calculates yearly stats.
It takes logs of previous year from 'MonthlyStats' and calculates

1. Total page views : number of times a page is viewed by the user.
2. Unique visits : it is counted if user visits the site for the first time or he/she revisit it after 30 minutes.
3. First time visits : it is counted if user visits the site for the first time.
4. Returning visits : it is counted if a previous user visits the site after 30 minutes.
5. Unique visitors : number of users who visited the site.

Then is saves them to 'YearlyStats'.

The script runs everyday after 12:00 AM.
"""

import datetime
from dashboard.models import MonthlyStats, YearlyStats 
from pytz import timezone
from django.conf import settings
from dateutil.relativedelta import relativedelta

# Timezone object used to localize time in current timezone
tz = timezone(settings.TIME_ZONE)

yesterday = datetime.datetime.now() - datetime.timedelta(1)
one_year_ago = datetime.datetime.now() - datetime.timedelta(yesterday.timetuple().tm_yday)

one_year_ago_min = datetime.datetime.combine(one_year_ago, datetime.time.min)
yesterday_max = datetime.datetime.combine(yesterday, datetime.time.max)

# Make datetimes timezone aware
one_year_ago_min = tz.localize(one_year_ago_min)
yesterday_max = tz.localize(yesterday_max)

# Getting data of the this or previous year from 'MonthlyStats'
previous_year_logs = MonthlyStats.objects.filter(datetime__range=(one_year_ago_min, yesterday_max)).order_by('-datetime') # Getting data of the date from log collection

# variables to store counts
page_views = 0
unique_visits = 0
first_time_visits = 0
returning_visits = 0
unique_visitors = 0

for log in previous_year_logs:
    page_views += log.page_views
    unique_visits += log.unique_visits
    first_time_visits += log.first_time_visits
    returning_visits += log.returning_visits
    unique_visitors += log.unique_visitors

# delete the stats if the stats of this year exist
YearlyStats.objects.filter(year=yesterday.year).delete()

previous_year_stats = YearlyStats() #YearlyStats object

previous_year_stats.datetime = tz.localize(yesterday) # localize yesterdays datetime using tz object
previous_year_stats.year = yesterday.year # get year of previous day 
previous_year_stats.page_views = page_views
previous_year_stats.unique_visits = unique_visits
previous_year_stats.first_time_visits = first_time_visits
previous_year_stats.returning_visits = returning_visits
previous_year_stats.unique_visitors = unique_visitors

previous_year_stats.save() # saving the calculations to database
