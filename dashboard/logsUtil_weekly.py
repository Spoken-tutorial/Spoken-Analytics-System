"""
This file takes logs from the dashboard_dailystats collection, calculates weekly logs stats
such as weekly_page_views, weekly_unique_visits, weekly_returning_visits and weekly_first_time_visits.
Then it stores them in the dashboard_weeklystats collection.

Terms: 
    Page views: number of times a page is viewed by the user.
    Unique visits: unique visit is counted if user visits the site for the first time or he/she revisit it after 30 minutes.
    First time visits: first time visit is counted if user visits the site for the first time.
    Unique visitors: number of users who visited the site.
"""
import datetime
from dashboard.models import Log, DailyStats, WeeklyStats

weeks = [] # Stores week number and year

logs = Log.objects.mongo_aggregate([{'$group': {'_id': {'woy': {'$isoWeek': '$datetime'}, 'year': { '$year': '$datetime' }}}}]) # woy = week of year

# Calculating weeks of which data is present
for log in logs:
    weeks.append(log['_id'])

# For each week calculating stats and storing them
for week in weeks:

    current_week = str(week['year']) + '-W' + str(week['woy'])
    next_week = str(week['year']) + '-W' + str(week['woy'] + 1)

    week_min = datetime.datetime.strptime(current_week + '-1', '%G-W%V-%u') # this week starting date and time
    week_max = datetime.datetime.strptime(next_week + '-1', '%G-W%V-%u') # this week ending date and time

    weekly_logs = Log.objects.filter(datetime__range=(week_min, week_max)).order_by('datetime') # Getting data of the week from log collection

    unique_visitors = [] # Stores unique ip addresses

    # Finding all unique ip addresses of this week
    for log in weekly_logs:
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
        for log in weekly_logs:
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

    weekly_stats = WeeklyStats() # WeeklyStats object

    weekly_stats.week_of_year = week['woy']
    weekly_stats.year = int(week['year'])
    weekly_stats.page_views = len(weekly_logs)
    weekly_stats.unique_visits = unique_visits
    weekly_stats.first_time_visits = first_time_total
    weekly_stats.returning_visits = returning_visits
    weekly_stats.unique_visitors = len(unique_visitors)
    
    weekly_stats.save() # saving the calculations to database
