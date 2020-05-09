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
from dashboard.models import Log, YearlyStats

years = [] # Stores all years for which data is present

logs = Log.objects.mongo_aggregate([{'$group': {'_id': {'year': {'$year': '$datetime'}}}}])

# Calculating number of years of which data is present
for log in logs:
    years.append(log['_id'])

# For each day calculating stats and storing them
for year in years:

    current_year = year['year']

    current_year_start = datetime.datetime(day= 1, month=1, year=current_year)
    current_year_end = datetime.datetime(day= 31, month=12, year=current_year)

    current_year_min_time = datetime.datetime.combine(current_year_start, datetime.time.min)
    current_year_max_time = datetime.datetime.combine(current_year_end, datetime.time.max)
    
    monthly_logs = Log.objects.filter(datetime__range=(current_year_min_time, current_year_max_time)).order_by('datetime') # Getting data of the date from log collection

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

    yearly_stats = YearlyStats() # YearlyStats object

    yearly_stats.date = current_year_min_time
    yearly_stats.year = current_year
    yearly_stats.page_views = len(monthly_logs)
    yearly_stats.unique_visits = unique_visits
    yearly_stats.first_time_visits = first_time_total
    yearly_stats.returning_visits = returning_visits
    yearly_stats.unique_visitors = len(unique_visitors)
    
    yearly_stats.save() # saving the calculations to database
