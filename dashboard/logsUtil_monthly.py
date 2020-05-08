"""
This file takes logs from the dashboard_dailystats collection, calculates daily logs stats
such as daily_page_views, daily_unique_visits, daily_returning_visits and daily_first_time_visits.
Then it stores them in the dashboard_dailystats collection.

Terms: 
    Page views: number of times a page is viewed by the user.
    Unique visits: unique visit is counted if user visits the site for the first time or he/she revisit it after 30 minutes.
    First time visits: first time visit is counted if user visits the site for the first time.
    Unique visitors: number of users who visited the site.
"""
import datetime
from dashboard.models import Log, MonthlyStats
from calendar import monthrange

months = [] # Stores all months for which data is present

logs = Log.objects.mongo_aggregate([{'$group': {'_id': {'month': {'$month': '$datetime'}, 'year': { '$year': '$datetime' }}}}])

# Calculating number of months of which data is present
for log in logs:
    months.append(log['_id'])

# For each day calculating stats and storing them
for month in months:

    current_month = month['month']
    current_year = month['year']

    current_month_start = datetime.datetime(day= 1, month=current_month, year=current_year)
    current_month_end = datetime.datetime(day= monthrange(current_year, current_month)[1], month=current_month, year=current_year)

    current_month_min_time = datetime.datetime.combine(current_month_start, datetime.time.min)
    current_month_max_time = datetime.datetime.combine(current_month_end, datetime.time.max)
    
    monthly_logs = Log.objects.filter(datetime__range=(current_month_min_time, current_month_max_time)).order_by('datetime') # Getting data of the date from log collection

    unique_visitors = [] # Stores unique ip addresses

    # Finding all unique ip addresses of this month
    for log in monthly_logs:
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
        for log in monthly_logs:
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

    monthly_stats = MonthlyStats() # MonthlyStats object

    monthly_stats.date = current_month_min_time
    monthly_stats.month_of_year = current_month
    monthly_stats.year = current_year
    monthly_stats.page_views = len(monthly_logs)
    monthly_stats.unique_visits = unique_visits
    monthly_stats.first_time_visits = first_time_total
    monthly_stats.returning_visits = returning_visits
    monthly_stats.unique_visitors = len(unique_visitors)
    
    monthly_stats.save() # saving the calculations to database
