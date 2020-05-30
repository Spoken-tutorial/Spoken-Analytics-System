"""
This script takes logs from the dashboard_dailystats collection, calculates daily logs stats
such as daily_page_views, daily_unique_visits, daily_returning_visits and daily_first_time_visits.
Then it stores them in the dashboard_dailystats collection.

Terms: 
    Page views: number of times a page is viewed by the user.
    Unique visits: unique visit is counted if user visits the site for the first time or he/she revisit it after 30 minutes.
    First time visits: first time visit is counted if user visits the site for the first time.
    Unique visitors: number of users who visited the site.
"""
import datetime
from dashboard.models import DailyStats, MonthlyStats
from calendar import monthrange
from pytz import timezone
from django.conf import settings
from celery import shared_task

# using bind=True on the shared_task decorator to turn the below function
# into a method of Task class. This lets us use self.retry for retrying
# failed tasks. Currently we are not retrying failed tasks.
@shared_task(bind=True)
def monthly(self):
    tz = timezone(settings.TIME_ZONE)

    yesterday = datetime.datetime.now() - datetime.timedelta(1) # eg. 2020-05-24 13:18:33.231161
    one_month_ago = datetime.datetime.now() - datetime.timedelta(yesterday.day) # eg. 2020-04-30 13:18:33.231161

    one_month_ago_min = datetime.datetime.combine(one_month_ago, datetime.time.min) # eg. 2020-05-01 00:00:00
    yesterday_max = datetime.datetime.combine(yesterday, datetime.time.max) # eg. 2020-05-24 23:59:59.999999

    # make datetimes timezone aware
    one_month_ago_min = tz.localize(one_month_ago_min)
    yesterday_max = tz.localize(yesterday_max)

    previous_month_logs = DailyStats.objects.filter(date__range=(one_month_ago_min, yesterday_max)).order_by('-datetime') # Getting data of the date from log collection

    # variables to store total values
    page_views = 0
    unique_visits = 0
    first_time_visits = 0
    returning_visits = 0
    unique_visitors = 0

    for log in previous_month_logs:
        page_views += log.page_views
        unique_visits += log.unique_visits
        first_time_visits += log.first_time_visits
        returning_visits += log.returning_visits
        unique_visitors += log.unique_visitors

    previous_month_stats = MonthlyStats()

    previous_month_stats.datetime = tz.localize(yesterday)
    previous_month_stats.month_of_year = yesterday.month
    previous_month_stats.year = yesterday.year
    previous_month_stats.page_views = page_views
    previous_month_stats.unique_visits = unique_visits
    previous_month_stats.first_time_visits = first_time_visits
    previous_month_stats.returning_visits = returning_visits
    previous_month_stats.unique_visitors = unique_visitors

    previous_month_stats.save()
