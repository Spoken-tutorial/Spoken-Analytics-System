import datetime
from dashboard.models import MonthlyStats, YearlyStats 
from pytz import timezone
from django.conf import settings
from dateutil.relativedelta import relativedelta

tz = timezone(settings.TIME_ZONE)

yesterday = datetime.datetime.now() - datetime.timedelta(1)
one_year_ago = datetime.datetime.now() - relativedelta(years=1)

print(yesterday)
print(one_year_ago)

one_year_ago_min = datetime.datetime.combine(one_year_ago, datetime.time.min)
yesterday_max = datetime.datetime.combine(yesterday, datetime.time.max)

print(one_year_ago_min)
print(yesterday_max)

# make datetimes timezone aware
one_year_ago_min = tz.localize(one_year_ago_min)
yesterday_max = tz.localize(yesterday_max)

previous_year_logs = MonthlyStats.objects.filter(datetime__range=(one_year_ago_min, yesterday_max)).order_by('-datetime') # Getting data of the date from log collection

# variables to store values
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

previous_year_stats = YearlyStats()

previous_year_stats.datetime = tz.localize(yesterday)
previous_year_stats.year = yesterday.year
previous_year_stats.page_views = page_views
previous_year_stats.unique_visits = unique_visits
previous_year_stats.first_time_visits = first_time_visits
previous_year_stats.returning_visits = returning_visits
previous_year_stats.unique_visitors = unique_visitors

previous_year_stats.save()
