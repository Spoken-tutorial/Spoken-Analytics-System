"""
This file takes logs from the main dashboard_log collection, calculates daily logs stats
such as daily_page_views, daily_unique_visits, daily_returning_visits and daily_first_time_visits.
Then it stores them in the dashboard_dailystats collection.
"""
import datetime
from dashboard.models import Log, DailyStats

dates = []
logs = Log.objects.all()

# Calculating number of days
for log in logs:
    if log.datetime.date() not in dates:
        print(log.datetime.date())
        dates.append(log.datetime.date())

# For each day calculating stats and storing them
for _date in dates:
    today_min = datetime.datetime.combine(_date, datetime.time.min)
    today_max = datetime.datetime.combine(_date, datetime.time.max)

    daily_logs = Log.objects.filter(datetime__range=(today_min, today_max)).order_by('datetime')

    unique_visitors = []

    for log in daily_logs:
        if log.ip_address not in unique_visitors:
            unique_visitors.append(log.ip_address)

    unique_visits = 0
    first_time = 0
    first_time_total = 0
    returning_visits = 0

    for ip in unique_visitors:
        first_time = 0
        for log in obj:
            if log.ip_address == ip and first_time == 0:
                prev_datetime = log.datetime
                first_time = 1
                first_time_total += 1
                unique_visits += 1
            elif log.ip_address == ip and first_time != 0 and (log.datetime - prev_datetime).seconds / 60 > 30:
                unique_visits += 1
                returning_visits += 1

    daily_stats = DailyStats()

    daily_stats.date = _date
    daily_stats.page_loads = len(obj)
    daily_stats.unique_visits = unique_visits
    daily_stats.first_time_visits = first_time_total
    daily_stats.returning_visits = returning_visits
    daily_stats.unique_visitors = len(unique_visitors)
    
    daily_stats.save()
