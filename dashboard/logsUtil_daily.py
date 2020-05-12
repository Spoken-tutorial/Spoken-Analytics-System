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
from dashboard.models import Log, DailyStats


dates = [] # Stores all dates for which data is present

logs = Log.objects.all() # Getting all the logs

print(datetime.datetime.now())

# Calculating number of days of which data is present
for log in logs:
    if log.datetime.date() not in dates:
        dates.append(log.datetime.date())

# For each day calculating stats and storing them
for _date in dates:

    today_min = datetime.datetime.combine(_date, datetime.time.min) # Days min datetime
    today_max = datetime.datetime.combine(_date, datetime.time.max) # Days max datetime

    daily_logs = Log.objects.filter(datetime__range=(today_min, today_max)).order_by('datetime') # Getting data of the date from log collection

    unique_visitors = [] # Stores unique ip addresses

    # Finding all unique ip addresses of this day
    for log in daily_logs:
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
        for log in daily_logs:
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

    daily_stats.date = _date
    daily_stats.page_views = len(daily_logs)
    daily_stats.unique_visits = unique_visits
    daily_stats.first_time_visits = first_time_total
    daily_stats.returning_visits = returning_visits
    daily_stats.unique_visitors = len(unique_visitors)
    
    daily_stats.save() # saving the calculations to database

print(datetime.datetime.now())