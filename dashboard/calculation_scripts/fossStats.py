"""
This script calculates
1. page views : number of times a foss is viewed by the user.
2. unique visits : it is counted if user views the foss for the first time or he/she reviews it after 30 minutes.
of different foss and save them to 'FossStats'.

The script runs everyday after 12:00 AM.
"""
import datetime
import re
from dashboard.models import Log, FossStats
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

foss = [] # Stores all foss for which data is present

logs = Log.objects.filter(datetime__range=(yesterday_min, yesterday_max)) # Getting the logs

# Calculating foss of which data is present
for log in logs:
    if log.path_info:
        # If path_info matches paths like /watch/*
        if log.path_info.find('/watch/') != -1:
            foss_name = re.split('/', log.path_info)
            if foss_name[2] not in foss:
                foss.append(foss_name[2])

# For each foss calculates stats
for foss_name in foss:

    # if there is no foss name then continue
    if foss_name == '':
        continue

    daily_logs = Log.objects.filter(path_info__contains=foss_name).filter(datetime__range=(yesterday_min, yesterday_max)).order_by('datetime') # Getting data of the date from log collection
    
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
                        prev_datetime = log.datetime
                        first_time = 1
                        unique_visits += 1
                    else:
                        # if same ip occurs after 30 minutes
                        if ((log.datetime - prev_datetime).seconds / 60) > 30:
                            unique_visits += 1
                    prev_datetime = log.datetime
        
        # saving the events stats
        foss_stats = FossStats()

        foss_stats.date = yesterday.date()
        foss_stats.datetime = tz.localize(yesterday)
        # Change foss names stored in path_info as 'Advance+C' to 'Advance C'
        foss_stats.foss_name = foss_name.replace("+", " ")
        foss_stats.page_views = len(daily_logs)
        foss_stats.unique_visits = unique_visits

        foss_stats.save()