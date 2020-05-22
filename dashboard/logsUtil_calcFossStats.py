"""
This script takes logs from the dashboard_dailystats collection, calculates daily logs stats 
(date and unique_visits) for different events.

Terms: 
    Unique visits: unique visit is counted if user visits the site for the first time or he/she revisit it after 30 minutes.
"""
import datetime
import re
from dashboard.models import Log, FossStats
from pytz import timezone
from django.conf import settings
from celery import shared_task


# using bind=True on the shared_task decorator to turn the below function
# into a method of Task class. This lets us use self.retry for retrying
# failed tasks. Currently we are not retrying failed tasks.
@shared_task(bind=True)
def calc_foss_stats (self):
    tz = timezone(settings.TIME_ZONE)

    dates = [] # Stores all dates for which data is present
    foss = [] # Stores all events for which data is present

    today = datetime.datetime.now()
    month_ago = today - datetime.timedelta(days=30)

    # make datetimes timezone aware
    today = tz.localize(today)
    month_ago = tz.localize(month_ago)

    logs = Log.objects.filter(datetime__range=(month_ago, today)) # Getting the logs

    # Calculating number of days of which data is present
    for log in logs:
        if log.path_info.find('/watch/') != -1:
            foss_name = re.split('/', log.path_info)
            if log.datetime.date() not in dates:
                dates.append(log.datetime.date())
            if foss_name[2] not in foss:
                foss.append(foss_name[2])

    for foss_name in foss:

        if foss_name == '':
            continue

        for _date in dates:

            today_min = datetime.datetime.combine(_date, datetime.time.min) # Days min datetime
            today_max = datetime.datetime.combine(_date, datetime.time.max) # Days max datetime

            # make datetimes timezone aware
            today_min = tz.localize(today_min)
            today_max = tz.localize(today_max)

            daily_logs = Log.objects.filter(path_info__contains=foss_name).filter(datetime__range=(today_min, today_max)).order_by('datetime') # Getting data of the date from log collection

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
            
            # saving the events stats
            foss_stats = FossStats()
            foss_stats.date = _date
            foss_stats.foss_name = foss_name
            foss_stats.page_views = len(daily_logs)
            foss_stats.unique_visits = unique_visits
            foss_stats.save()