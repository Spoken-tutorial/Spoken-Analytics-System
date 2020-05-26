import datetime
from dashboard.models import Log, DailyStats
from pytz import timezone
from django.conf import settings

tz = timezone(settings.TIME_ZONE)

yesterday = datetime.datetime.now() - datetime.timedelta(1)

yesterday_min = datetime.datetime.combine(yesterday, datetime.time.min) # Yesterdays min datetime
yesterday_max = datetime.datetime.combine(yesterday, datetime.time.max) # Yesterdays max datetime

# make datetimes timezone aware
yesterday_min = tz.localize(yesterday_min)
yesterday_max = tz.localize(yesterday_max)

previous_day_logs = Log.objects.filter(datetime__range=(yesterday_min, yesterday_max)).order_by('-datetime') # Getting data of the date from log collection

unique_visitors = [] # Stores unique ip addresses

# Finding all unique ip addresses of this day
for log in previous_day_logs:
    if log.ip_address not in unique_visitors:
        unique_visitors.append(log.ip_address)

# variables to store counts
unique_visits = 0
first_time = 0
first_time_total = 0
returning_visits = 0

# caculating stats according to ip addresses
for ip in unique_visitors:
    first_time = 0
    for log in previous_day_logs:
        if log.ip_address == ip:
            # if ip is found for the first time
            if first_time == 0:
                prev_datetime = log.datetime
                first_time = 1
                first_time_total += 1
                unique_visits += 1
            else:
                # if same ip occurs within time differce of 30 minutes
                if (log.datetime - prev_datetime).seconds / 60 > 30:
                    prev_datetime = log.datetime
                    returning_visits += 1
                    unique_visits += 1

daily_stats = DailyStats() # DailyStats object

daily_stats.datetime = tz.localize(yesterday)
daily_stats.date = yesterday.date()
daily_stats.page_views = len(previous_day_logs)
daily_stats.unique_visits = unique_visits
daily_stats.first_time_visits = first_time_total
daily_stats.returning_visits = returning_visits
daily_stats.unique_visitors = len(unique_visitors)

daily_stats.save() # saving the calculations to database