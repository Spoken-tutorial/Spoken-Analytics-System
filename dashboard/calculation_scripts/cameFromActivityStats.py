"""
This script calculates came from activity stats.
It takes logs from 'Log', calculates came from activity stats and 
stores them to 'CameFromActivity'.

The script runs everyday after 12:05 AM.
"""

import datetime
from dashboard.models import Log, CameFromActivity
from pytz import timezone
from django.conf import settings
from celery import shared_task

@shared_task(bind=True)
def came_from_activity_statistics(self):
    
    # Timezone object used to localize time in current timezone
    tz = timezone(settings.TIME_ZONE)

    yesterday = datetime.datetime.now() - datetime.timedelta(1)

    yesterday_min = datetime.datetime.combine(yesterday, datetime.time.min) # Yesterdays min datetime
    yesterday_max = datetime.datetime.combine(yesterday, datetime.time.max) # Yesterdays max datetime

    # make datetimes timezone aware
    yesterday_min = tz.localize(yesterday_min)
    yesterday_max = tz.localize(yesterday_max)

    yesterdays_logs = Log.oip_logsbjects.filter(datetime__range=(yesterday_min, yesterday_max)).order_by('-datetime') # Getting data of the date from log collection

    for log in yesterdays_logs:
        # if referrer is present
        if log.referrer:
            # store the came from log only if referring in present and is not from spoken website
            if not log.referrer.find('https://spoken-tutorial.org') != -1 and not log.referrer.find('(No referring link)') != -1:
                came_from_stats = CameFromActivity()
                came_from_stats.datetime = log.datetime
                came_from_stats.referrer = log.referrer
                came_from_stats.entry_page = log.path_info
                came_from_stats.save()