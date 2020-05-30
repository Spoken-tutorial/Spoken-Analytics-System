"""
This script takes logs from the dashboard_dailystats collection, calculates daily logs stats 
(date and unique_visits) for different events.
Terms: 
    Unique visits: unique visit is counted if user visits the site for the first time or he/she revisit it after 30 minutes.
"""
import datetime
from dashboard.models import ExitLinkActivity, ExitLinkStats
from django.utils.timezone import get_current_timezone
from pytz import timezone
from django.conf import settings

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