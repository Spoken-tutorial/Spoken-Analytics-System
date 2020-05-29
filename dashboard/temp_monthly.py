import datetime
from dashboard.models import DailyStats, MonthlyStats
from pytz import timezone
from django.conf import settings

tz = timezone(settings.TIME_ZONE)

yesterday = datetime.datetime.now() - datetime.timedelta(1)
one_month_ago = datetime.datetime.now() - datetime.timedelta(yesterday.day)

one_month_ago_min = datetime.datetime.combine(one_month_ago, datetime.time.min)
yesterday_max = datetime.datetime.combine(yesterday, datetime.time.max)

# make datetimes timezone aware
one_month_ago_min = tz.localize(one_month_ago_min)
yesterday_max = tz.localize(yesterday_max)

previous_month_logs = DailyStats.objects.filter(date__range=(one_month_ago_min, yesterday_max)).order_by('-datetime') # Getting data of the date from log collection

# variables to store values
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