"""
This script calculates came from activity stats.
It takes logs from 'Log', calculates came from activity stats and 
stores them to 'CameFromActivity'.
"""

import datetime
from dashboard.models import Log, CameFromActivity
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

    for log in ip_logs:
        # store the came from log only if referring in present and is not from spoken website
        if not log.referrer.find('https://spoken-tutorial.org') != -1 and not log.referrer.find('(No referring link)') != -1:
            came_from_stats = CameFromActivity()
            came_from_stats.datetime = log.datetime
            came_from_stats.referrer = log.referrer
            came_from_stats.entry_page = log.path_info
            came_from_stats.save()