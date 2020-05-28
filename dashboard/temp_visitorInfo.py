import datetime
from dashboard.models import Log, VisitorInfo
from pytz import timezone
from django.conf import settings

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

flag = 0
for ip_address in ip_addresses:

    ip_logs = Log.objects.filter(ip_address=ip_address).filter(datetime__range=(yesterday_min, yesterday_max)).order_by('datetime')

    prev_datetime = ip_logs.first().datetime
    first_datetime = ip_logs.first().datetime
    path = []
    referrer = '(No referring link)'
    returning_visits = 0

    for log in ip_logs:
        path += [{'datetime': log.datetime, 'referrer': log.referrer, 'page_url': log.path_info}]
        # if same ip occurs after 30 minutes
        if (log.datetime - prev_datetime).seconds / 60 > 30:
            returning_visits += 1

            visitor_info_stats = VisitorInfo() # DailyStats object

            visitor_info_stats.datetime = log.datetime
            visitor_info_stats.referrer = referrer
            visitor_info_stats.city = ip_logs.first().city
            visitor_info_stats.region = ip_logs.first().region
            visitor_info_stats.country = ip_logs.first().country
            visitor_info_stats.ip_address = ip_logs.first().ip_address
            visitor_info_stats.returning_visits = returning_visits
            visitor_info_stats.browser = ip_logs.first().browser_family + " " + ip_logs.first().browser_version
            visitor_info_stats.os = ip_logs.first().os_family + " " + ip_logs.first().os_version
            visitor_info_stats.device = ip_logs.first().device_family + " " + ip_logs.first().device_type
            visitor_info_stats.visit_length_sec = (log.datetime - first_datetime).seconds
            visitor_info_stats.path = path

            visitor_info_stats.save()

            first_datetime = log.datetime
            flag = 1
            path = []
        else:
            referrer = log.referrer

        prev_datetime = log.datetime


    if flag == 1:
        flag = 0
        continue
        
    visitor_info_stats = VisitorInfo() # DailyStats object

    visitor_info_stats.datetime = log.datetime
    visitor_info_stats.referrer = referrer
    visitor_info_stats.city = ip_logs.first().city
    visitor_info_stats.region = ip_logs.first().region
    visitor_info_stats.country = ip_logs.first().country
    visitor_info_stats.ip_address = ip_logs.first().ip_address
    visitor_info_stats.returning_visits = returning_visits
    visitor_info_stats.browser = ip_logs.first().browser_family + " " + ip_logs.first().browser_version
    visitor_info_stats.os = ip_logs.first().os_family + " " + ip_logs.first().os_version
    visitor_info_stats.device = ip_logs.first().device_family + " " + ip_logs.first().device_type
    visitor_info_stats.visit_length_sec = (log.datetime - first_datetime).seconds
    visitor_info_stats.path = path

    visitor_info_stats.save()
    break