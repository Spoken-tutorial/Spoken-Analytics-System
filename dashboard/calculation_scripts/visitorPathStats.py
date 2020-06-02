"""
This script calculates visitor path stats.
It takes logs from 'Log', calculates visitor path stats and 
stores them to 'VisitorPath'.
"""

import datetime
from dashboard.models import Log, VisitorPath
from pytz import timezone
from django.conf import settings

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

    prev_datetime = ip_logs.first().datetime
    path = []
    visit_num = 0

    for log in ip_logs:
        # if same ip occurs after 30 minutes
        if (log.datetime - prev_datetime).seconds / 60 > 30:

            path += [{'datetime': log.datetime, 'referrer': log.referrer, 'page_url': log.path_info}]
            visit_num += 1

            visitor_path_stats = VisitorPath() # DailyStats object

            visitor_path_stats.datetime = log.datetime
            visitor_path_stats.city = ip_logs.first().city
            visitor_path_stats.region = ip_logs.first().region
            visitor_path_stats.country = ip_logs.first().country
            visitor_path_stats.ip_address = ip_logs.first().ip_address
            visitor_path_stats.visit_num = visit_num
            visitor_path_stats.browser = ip_logs.first().browser_family + " " + ip_logs.first().browser_version
            visitor_path_stats.os = ip_logs.first().os_family + " " + ip_logs.first().os_version
            visitor_path_stats.device = ip_logs.first().device_family + " " + ip_logs.first().device_type
            visitor_path_stats.path = path
            visitor_path_stats.save()

            path = []
        else:
            path += [{'datetime': log.datetime, 'referrer': log.referrer, 'page_url': log.path_info}]

        prev_datetime = log.datetime