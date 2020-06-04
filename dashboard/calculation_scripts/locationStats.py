"""
This script takes logs from the 'Log' and calculates no of page loads from different locations.

The script runs everyday after 12:05 AM.
"""

import datetime
from dashboard.models import Log, RegionStats, CityStats
from django.db.models import Count
from pytz import timezone
from django.conf import settings
from celery import shared_task

@shared_task(bind=True)
def location_statistics(self):
    
    # Timezone object used to localize time in current timezone
    tz = timezone(settings.TIME_ZONE)

    yesterday = datetime.datetime.now() - datetime.timedelta(1)

    yesterday_min = datetime.datetime.combine(yesterday, datetime.time.min) # Yesterdays min datetime
    yesterday_max = datetime.datetime.combine(yesterday, datetime.time.max) # Yesterdays max datetime

    # make datetimes timezone aware
    yesterday_min = tz.localize(yesterday_min)
    yesterday_max = tz.localize(yesterday_max)

    # Getting yesterdays data from log collection
    yesterdays_logs = Log.objects.filter(datetime__range=(yesterday_min, yesterday_max)).order_by('datetime') 


    # Calculating city stats (which city got how much page views)
    city_stats = yesterdays_logs.values('city').order_by('city').annotate(count=Count('city'))

    # Saving the stats
    for stats in city_stats:
        city_stats = CityStats()
        city_stats.datetime = tz.localize(yesterday)
        city_stats.city = stats['city']
        city_stats.page_views = stats['count']
        city_stats.save()

    # Calculating region stats (which region got how much page views)
    region_stats = yesterdays_logs.values('region').order_by('region').annotate(count=Count('region'))

    # Saving the stats
    for stats in region_stats:
        region_stats = RegionStats()
        region_stats.datetime = tz.localize(yesterday)
        region_stats.region = stats['region']
        region_stats.page_views = stats['count']
        region_stats.save()