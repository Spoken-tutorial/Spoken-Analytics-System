import datetime
from dashboard.models import Log, VisitorActivity
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

# Finding all unique ip addresses of this day
for log in yesterdays_logs:
    if log.ip_address not in ip_addresses:
        ip_addresses.append(log.ip_address)

for ip_address in ip_addresses:

    ip_logs = Log.objects.filter(ip_address=ip_address).filter(datetime__range=(yesterday_min, yesterday_max)).order_by('datetime')

    total_visits = 0
    first_time = 0
    first_time_total = 0
    returning_visits = 0

    for log in ip_logs:
        # if ip is found for the first time
        if first_time == 0:
            prev_datetime = log.datetime
            total_visits += 1
            first_time = 1
            first_datetime = log.datetime
            last_datetime = log.datetime
            referrer = log.referrer
            entry_page = log.path_info
        else:
            # if same ip occurs after 30 minutes
            if (log.datetime - prev_datetime).seconds / 60 > 30:
                total_visits += 1
                first_datetime = last_datetime
                last_datetime = log.datetime
                referrer = log.referrer
                entry_page = log.path_info
            else:
                last_datetime = log.datetime
        prev_datetime = log.datetime


    print("Date: ", yesterday.date())
    print("Page Views: ", len(ip_logs))
    print("Total Visits: ", total_visits)
    print("Latest Page View: ", ip_logs.last().datetime)
    print("City: ", ip_logs.first().city)
    print("Region: ", ip_logs.first().region)
    print("Country: ", ip_logs.first().country)
    print("Visit length: ", (last_datetime - first_datetime).seconds)
    print("IP: ", ip_address)
    print("Browser: ", ip_logs.first().browser_family, ip_logs.first().browser_version)
    print("OS: ", ip_logs.first().os_family, ip_logs.first().os_version)
    print("Device: ", ip_logs.first().device_family, ip_logs.first().device_type)
    print("Referrer: ", referrer)
    print("Entry Page: ", entry_page)
    print("Latest Page: ", ip_logs.last().path_info)

    visitor_activity_stats = VisitorActivity() # DailyStats object

    visitor_activity_stats.datetime = first_datetime
    visitor_activity_stats.page_views = len(ip_logs)
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