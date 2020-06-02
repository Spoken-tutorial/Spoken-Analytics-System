"""
This script calculates
1. page views : number of times a page is viewed by the user.
2. unique visits : it is counted if user visits the site for the first time or he/she revisit it after 30 minutes.
of different pages and save them to 'EventStats'.

The script runs everyday after 12:00 AM.
"""
import datetime
from dashboard.models import Log, EventStats
from pytz import timezone
from django.conf import settings
from dashboard.events_info import get_title_of_event

# Timezone object used to localize time in current timezone
tz = timezone(settings.TIME_ZONE)

yesterday = datetime.datetime.now() - datetime.timedelta(1)

yesterday_min = datetime.datetime.combine(yesterday, datetime.time.min) # Yesterdays min datetime
yesterday_max = datetime.datetime.combine(yesterday, datetime.time.max) # Yesterdays max datetime

# make datetimes timezone aware
yesterday_min = tz.localize(yesterday_min)
yesterday_max = tz.localize(yesterday_max)

paths = [] # Stores all paths for which data is present

logs = Log.objects.filter(datetime__range=(yesterday_min, yesterday_max)) # Getting the logs

# Finding paths of which data is present
for log in logs:
    if log.path_info not in paths:
        paths.append(log.path_info)

# loop through each path found
for path in paths:

    # Getting data of the path from 'Log'
    daily_logs = Log.objects.filter(path_info=path).filter(datetime__range=(yesterday_min, yesterday_max)).order_by('datetime') 
    
    # if logs are found
    if daily_logs:
        unique_visitors = [] # Stores unique ip addresses

        # Finding all unique ip addresses of this day
        for log in daily_logs:
            if log.ip_address not in unique_visitors:
                unique_visitors.append(log.ip_address)

        # variables to store counts
        unique_visits = 0
        first_time = 0

        # caculating stats according to ip addresses
        for ip in unique_visitors:
            first_time = 0
            for log in daily_logs:
                if ip == log.ip_address:
                    # if ip is found for the first time
                    if first_time == 0:
                        first_time = 1
                        unique_visits += 1
                    else:
                        # if same ip occurs after 30 minutes
                        if ((log.datetime - prev_datetime).seconds / 60) > 30:
                            unique_visits += 1
                    prev_datetime = log.datetime
        
        # saving the events stats
        event_stats = EventStats()

        event_stats.datetime = tz.localize(yesterday)
        event_stats.date = yesterday.date()
        event_stats.path_info = path

        if daily_logs.first().page_title != "":
            title = daily_logs.first().page_title
        else:
            title = get_title_of_event(daily_logs.first().event_name)

        event_stats.page_title = title
        event_stats.page_views = len(daily_logs)
        event_stats.unique_visits = unique_visits

        event_stats.save()