"""
This script takes logs from the 'Log' calculates came from stats for different referrers
and stored them to 'CameFromStats'.

The script runs everyday after 12:05 AM.
"""
import datetime
from dashboard.models import Log, CameFromStats
from django.utils.timezone import get_current_timezone
from pytz import timezone
from django.conf import settings
from celery import shared_task

@shared_task(bind=True)
def came_from_statistics(self):
    
    tz = timezone(settings.TIME_ZONE)

    yesterday = datetime.datetime.now() - datetime.timedelta(1)

    yesterday_min = datetime.datetime.combine(yesterday, datetime.time.min) # Yesterdays min datetime
    yesterday_max = datetime.datetime.combine(yesterday, datetime.time.max) # Yesterdays max datetime

    # make datetimes timezone aware
    yesterday_min = tz.localize(yesterday_min)
    yesterday_max = tz.localize(yesterday_max)

    referrers = [] # Stores all paths for which data is present

    logs = Log.objects.filter(datetime__range=(yesterday_min, yesterday_max)) # Getting the logs

    # Calculating paths of which data is present
    for log in logs:
        if log.referrer not in referrers:
            referrers.append(log.referrer)

    for referrer in referrers:
        # if referrer is present
        if log.referrer:
            # if referring url is not of spoken website
            if not log.referrer.find('https://spoken-tutorial.org') != -1:

                referrer_logs = Log.objects.filter(referrer=referrer).filter(datetime__range=(yesterday_min, yesterday_max)).order_by('datetime') # Getting data of the date from log collection
                
                came_from_stats = CameFromStats()

                came_from_stats.datetime = tz.localize(yesterday)
                came_from_stats.referrer = referrer
                came_from_stats.page_views = len(referrer_logs)

                came_from_stats.save()