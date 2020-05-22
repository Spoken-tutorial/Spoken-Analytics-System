"""
This script takes logs from the dashboard_log collection, calculates no of page loads from different locations.
"""
import datetime
from dashboard.models import Log, RegionStats, CityStats
from django.db.models import Count
from celery import shared_task

# using bind=True on the shared_task decorator to turn the below function
# into a method of Task class. This lets us use self.retry for retrying
# failed tasks. Currently we are not retrying failed tasks.
@shared_task(bind=True)
def calc_loc_stats ():
    city_stats = Log.objects.values('city').order_by('city').annotate(count=Count('city'))

    for stats in city_stats:
        city_stats = CityStats()
        city_stats.city = stats['city']
        city_stats.page_views = stats['count']
        city_stats.save()

    region_stats = Log.objects.values('region').order_by('region').annotate(count=Count('region'))

    for stats in region_stats:
        region_stats = RegionStats()
        region_stats.region = stats['region']
        region_stats.page_views = stats['count']
        region_stats.save()




    # Finding regions and cities of which data is present
    # for log in logs:
    #     if log.city not in cities:
    #         cities.append(log.city)
    #     if log.region not in regions:
    #         regions.append(log.region)

    # for city in cities:

    #         daily_logs = Log.objects.filter(event_name=event[0]).filter(datetime__range=(today_min, today_max)).order_by('datetime') # Getting data of the date from log collection

    #         unique_visitors = [] # Stores unique ip addresses

    #         # Finding all unique ip addresses of this day
    #         for log in daily_logs:
    #             if log.ip_address not in unique_visitors:
    #                 unique_visitors.append(log.ip_address)

    #         # variables to store counts
    #         unique_visits = 0
    #         first_time = 0

    #         # caculating stats according to ip addresses
    #         for ip in unique_visitors:
    #             first_time = 0
    #             for log in daily_logs:
    #                 if log.ip_address == ip:
    #                     # if ip is found for the first time
    #                     if first_time == 0:
    #                         prev_datetime = log.datetime
    #                         unique_visits += 1
    #                     else:
    #                         # if same ip occurs within time differce of 30 minutes
    #                         if (log.datetime - prev_datetime).seconds / 60 > 30:
    #                             prev_datetime = log.datetime
    #                             unique_visits += 1
            
    #         # saving the events stats
    #         event_stats = EventStats()
    #         event_stats.date = _date
    #         event_stats.event_name = event[0]
    #         event_stats.path_info = event[1]
    #         event_stats.unique_visits = unique_visits
    #         event_stats.save()