"""
This script takes logs from the dashboard_dailystats collection, calculates daily logs stats 
(date and unique_visits) for different events.

Terms: 
    Unique visits: unique visit is counted if user visits the site for the first time or he/she revisit it after 30 minutes.
"""
import datetime
from dashboard.models import Log, EventStats
from django.utils.timezone import get_current_timezone
from pytz import timezone
from django.conf import settings
from celery import shared_task
from dashboard.events_info import events_titles


# using bind=True on the shared_task decorator to turn the below function
# into a method of Task class. This lets us use self.retry for retrying
# failed tasks. Currently we are not retrying failed tasks.
@shared_task(bind=True)
def calc_event_stats (self):
    tz = timezone(settings.TIME_ZONE)

    yesterday = datetime.datetime.now() - datetime.timedelta(1)

    yesterday_min = datetime.datetime.combine(yesterday, datetime.time.min) # Yesterdays min datetime
    yesterday_max = datetime.datetime.combine(yesterday, datetime.time.max) # Yesterdays max datetime

    # make datetimes timezone aware
    yesterday_min = tz.localize(yesterday_min)
    yesterday_max = tz.localize(yesterday_max)

    logs = Log.objects.filter(datetime__range=(yesterday_min, yesterday_max)) # Getting the logs

    stats = []

    for event in events_titles:
        yesterdays_logs = logs.filter(event_name=event[0]).order_by('datetime') # Getting data of the date from log collection

        unique_visitors = [] # Stores unique ip addresses

        # Finding all unique ip addresses of this day
        for log in yesterdays_logs:
            if log.ip_address not in unique_visitors:
                unique_visitors.append(log.ip_address)
        # variables to store counts
        unique_visits = 0
        first_time = 0

        # caculating stats according to ip addresses
        for ip in unique_visitors:
            first_time = 0
            for log in yesterdays_logs:
                if log.ip_address == ip:
                    # if ip is found for the first time
                    if first_time == 0:
                        prev_datetime = log.datetime
                        unique_visits += 1
                    else:
                        # if same ip occurs within time differce of 30 minutes
                        if (log.datetime - prev_datetime).seconds / 60 > 30:
                            prev_datetime = log.datetime
                            unique_visits += 1
        
        stats += [{
            'event_name': event[0],
            'page_title': event[1],
            'path_info': '',
            'page_views': len(yesterdays_logs),
            'unique_visits': unique_visits,
        }]

    # saving the events stats
    event_stats = EventStats()
    event_stats.date = yesterday.date()
    event_stats.datetime = tz.localize(datetime.datetime.now())
    event_stats.event = stats
    event_stats.save()