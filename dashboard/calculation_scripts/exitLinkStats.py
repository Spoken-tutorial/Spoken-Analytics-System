"""
*** Important ***
We aren't using this script as of now.

The exit link activity and exit link stats features are to be
implemented in next version.

This script calculates exit link stats.
It takes logs from 'ExitLinkActivity', calculates exit link stats and 
stores them to 'ExitLinkStats'.
"""

import datetime
from dashboard.models import ExitLinkActivity, ExitLinkStats
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

exit_links = [] # Stores all paths for which data is present

logs = ExitLinkActivity.objects.filter(datetime__range=(yesterday_min, yesterday_max)) # Getting the logs

# Calculating paths of which data is present
for log in logs:
    if log.exit_link_clicked not in exit_links:
        exit_links.append(log.exit_link_clicked)

for link in exit_links:

    total_exit_link = ExitLinkActivity.objects.filter(exit_link_clicked=link).filter(datetime__range=(yesterday_min, yesterday_max)).count() # Getting data of the date from log collection
    
    exit_link_stats = ExitLinkStats()

    exit_link_stats.datetime = tz.localize(yesterday)
    exit_link_stats.exit_link = link
    exit_link_stats.page_views = total_exit_link

    exit_link_stats.save()