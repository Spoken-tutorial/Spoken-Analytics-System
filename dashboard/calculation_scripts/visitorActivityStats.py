"""
This script calculates visitor activity stats.
It takes logs from 'Log', calculates visitor activity stats and 
stores them to 'VisitorAcitivty'.

The script runs everyday after 12:05 AM.
"""

import datetime
from dashboard.models import Log, VisitorActivity
from pytz import timezone
from django.conf import settings
from celery import shared_task

@shared_task(bind=True)
def visitor_activity_statistics(self):
    
    # Timezone object used to localize time in current timezone
    tz = timezone(settings.TIME_ZONE)

    yesterday = datetime.datetime.now() - datetime.timedelta(1)

    yesterday_min = datetime.datetime.combine(yesterday, datetime.time.min) # Yesterdays min datetime
    yesterday_max = datetime.datetime.combine(yesterday, datetime.time.max) # Yesterdays max datetime

    # Make datetimes timezone aware
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

        prev_datetime = ip_logs.first().datetime
        first_datetime = ip_logs.first().datetime
        last_datetime = ip_logs.first().datetime
        referrer = '(No referring link)'
        total_visits = 1
        page_views = 1
        entry_page = ip_logs.first().path_info
        flag = 0

        for log in ip_logs:
            # if same ip occurs after 30 minutes
            if (log.datetime - prev_datetime).seconds / 60 > 30:

                visitor_activity_stats = VisitorActivity() # DailyStats object

                visitor_activity_stats.datetime = first_datetime
                visitor_activity_stats.page_views = page_views
                visitor_activity_stats.total_visits = total_visits + 1
                visitor_activity_stats.latest_page_view =  log.datetime
                visitor_activity_stats.city = ip_logs.first().city
                visitor_activity_stats.region = ip_logs.first().region
                visitor_activity_stats.country = ip_logs.first().country
                visitor_activity_stats.visit_length_sec = (last_datetime - first_datetime).seconds
                visitor_activity_stats.ip_address = ip_address
                visitor_activity_stats.browser = ip_logs.first().browser_family + " " + ip_logs.first().browser_version
                visitor_activity_stats.os = ip_logs.first().os_family + " " + ip_logs.first().os_version
                visitor_activity_stats.device = ip_logs.first().device_family + " " + ip_logs.first().device_type
                visitor_activity_stats.referrer = referrer
                visitor_activity_stats.entry_page = entry_page
                visitor_activity_stats.latest_page = log.path_info

                visitor_activity_stats.save() # saving the calculations to database

                first_datetime = log.datetime
                last_datetime = log.datetime
                total_visits += 1
                page_views = 1
                flag = 1
            else:
                page_views += 1
                referrer = log.referrer
                last_datetime = log.datetime
                if flag == 1:
                    flag = 0
                    entry_page = log.path_info

            prev_datetime = log.datetime

        if flag == 1:
            flag = 0
            continue
        else: 
            visitor_activity_stats = VisitorActivity() # DailyStats object

            visitor_activity_stats.datetime = first_datetime
            visitor_activity_stats.page_views = page_views
            visitor_activity_stats.total_visits = total_visits
            visitor_activity_stats.latest_page_view =  ip_logs.last().datetime
            visitor_activity_stats.city = ip_logs.first().city
            visitor_activity_stats.region = ip_logs.first().region
            visitor_activity_stats.country = ip_logs.first().country
            visitor_activity_stats.visit_length_sec = (last_datetime - first_datetime).seconds
            visitor_activity_stats.ip_address = ip_address
            visitor_activity_stats.browser = ip_logs.first().browser_family + " " + ip_logs.first().browser_version
            visitor_activity_stats.os = ip_logs.first().os_family + " " + ip_logs.first().os_version
            visitor_activity_stats.device = ip_logs.first().device_family + " " + ip_logs.first().device_type
            visitor_activity_stats.referrer = referrer
            visitor_activity_stats.entry_page = entry_page
            visitor_activity_stats.latest_page = ip_logs.last().path_info

            visitor_activity_stats.save() # saving the calculations to database