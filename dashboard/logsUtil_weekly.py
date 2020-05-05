"""
This file takes logs from the dashboard_dailystats collection, calculates weekly logs stats
such as weekly_page_views, weekly_unique_visits, weekly_returning_visits and weekly_first_time_visits.
Then it stores them in the dashboard_weeklystats collection.
"""
import datetime
from dashboard.models import Log, DailyStats, WeeklyStats

weeks = []
# logs = Log.objects.mongo_aggregate([{'$project': { 'week': { '$week': '$datetime' } }}
#     , {'$group': { '_id': '$_id', 'week': '$week'}}])

logs = Log.objects.mongo_aggregate([{'$group': {'_id': {'woy': {'$isoWeek': '$datetime'}, 'year': { '$year': '$datetime' }}}}]) # woy = week of year

for log in logs:
    weeks.append(log['_id'])

print(weeks[0]['year'])

# For each day calculating stats and storing them
for week in weeks:
    this_week = str(week['year']) + '-W' + str(week['woy'])
    next_week = str(week['year']) + '-W' + str(week['woy'] + 1)
    week_min = datetime.datetime.strptime(this_week + '-1', '%G-W%V-%u')
    week_max = datetime.datetime.strptime(next_week + '-1', '%G-W%V-%u')
    # today_min = datetime.datetime.combine(_date, datetime.time.min)
    # today_max = datetime.datetime.combine(_date, datetime.time.max)

    weekly_logs = Log.objects.filter(datetime__range=(week_min, week_max)).order_by('datetime')

    unique_visitors = []

    for log in weekly_logs:
        if log.ip_address not in unique_visitors:
            unique_visitors.append(log.ip_address)

    unique_visits = 0
    first_time = 0
    first_time_total = 0
    returning_visits = 0

    for ip in unique_visitors:
        first_time = 0
        for log in weekly_logs:
            if log.ip_address == ip and first_time == 0:
                prev_datetime = log.datetime
                first_time = 1
                first_time_total += 1
                unique_visits += 1
            elif log.ip_address == ip and first_time != 0 and (log.datetime - prev_datetime).seconds / 60 > 30:
                unique_visits += 1
                returning_visits += 1

    weekly_stats = WeeklyStats()

    weekly_stats.week_of_year = week['woy']
    weekly_stats.year = int(week['year'])
    weekly_stats.page_loads = len(weekly_logs)
    weekly_stats.unique_visits = unique_visits
    weekly_stats.first_time_visits = first_time_total
    weekly_stats.returning_visits = returning_visits
    weekly_stats.unique_visitors = len(unique_visitors)
    
    weekly_stats.save()
