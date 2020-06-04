"""
This script calculates page view activity stats.
It takes logs from 'Log', calculates page view stats and 
stores them to 'PageViewActivity'.

The script runs everyday after 12:05 AM.
"""

import datetime
from dashboard.models import Log, PageViewActivity
from pytz import timezone
from django.conf import settings

from celery import shared_task

@shared_task(bind=True)
def page_view_activity_statistics(self):
    
    # Timezone object used to localize time in current timezone
    tz = timezone(settings.TIME_ZONE)

    yesterday = datetime.datetime.now() - datetime.timedelta(1)

    yesterday_min = datetime.datetime.combine(yesterday, datetime.time.min) # Yesterdays min datetime
    yesterday_max = datetime.datetime.combine(yesterday, datetime.time.max) # Yesterdays max datetime

    # make datetimes timezone aware
    yesterday_min = tz.localize(yesterday_min)
    yesterday_max = tz.localize(yesterday_max)

    yesterdays_logs = Log.objects.filter(datetime__range=(yesterday_min, yesterday_max)).order_by('-datetime') # Getting data of the date from log collection

    ip_addresses = [] # Stores unique ip addresses

    # Finding all unique ip addresses of previous day
    for log in yesterdays_logs:
        if log.ip_address not in ip_addresses:
            ip_addresses.append(log.ip_address)

    for ip_address in ip_addresses:

        ip_logs = Log.objects.filter(ip_address=ip_address).filter(datetime__range=(yesterday_min, yesterday_max)).order_by('datetime')

        for log in ip_logs:
            page_view_stats = PageViewActivity()

            page_view_stats.datetime = log.datetime
            page_view_stats.browser = ip_logs.first().browser_family + " " + ip_logs.first().browser_version
            page_view_stats.os = ip_logs.first().os_family + " " + ip_logs.first().os_version
            page_view_stats.device = ip_logs.first().device_family + " " + ip_logs.first().device_type
            page_view_stats.city = ip_logs.first().city
            page_view_stats.region = ip_logs.first().region
            page_view_stats.country = ip_logs.first().country
            page_view_stats.ip_address = ip_logs.first().ip_address
            page_view_stats.page_name = log.page_title
            page_view_stats.page_url = log.path_info
            page_view_stats.referrer = log.referrer
            
            page_view_stats.save()