import datetime
from dashboard.models import Log, BrowserStats, OSStats, PlatformStats
from pytz import timezone
from django.conf import settings

tz = timezone(settings.TIME_ZONE)

yesterday = datetime.datetime.now() - datetime.timedelta(1)

yesterday_min = datetime.datetime.combine(yesterday, datetime.time.min) # Yesterdays min datetime
yesterday_max = datetime.datetime.combine(yesterday, datetime.time.max) # Yesterdays max datetime

# make datetimes timezone aware
yesterday_min = tz.localize(yesterday_min)
yesterday_max = tz.localize(yesterday_max)

# Getting yesterdays data from log collection
yesterdays_logs = Log.objects.filter(datetime__range=(yesterday_min, yesterday_max))

browsers = [] # Stores list of browsers
os_s = []
platforms = []

# Finding all unique ip addresses of this day
for log in yesterdays_logs:
    if (log.browser_family, log.browser_version) not in browsers:
        browsers.append((log.browser_family, log.browser_version))
    if (log.os_family, log.os_version) not in os_s:
        os_s.append((log.os_family, log.os_version))
    if log.device_type not in platforms:
        platforms.append(log.device_type)

# Calculating logs and storing them
for browser in browsers:

    browser_logs = yesterdays_logs.filter(browser_family=browser[0], browser_version=browser[1])

    browser_stats = BrowserStats()
    browser_stats.datetime = tz.localize(yesterday)
    browser_stats.browser_type = browser_logs.first().device_type
    browser_stats.name = browser[0] + " " + browser[1]
    browser_stats.page_views = len(browser_logs)
    browser_stats.save()

for os in os_s:

    os_logs = yesterdays_logs.filter(os_family=os[0], os_version=os[1])

    os_stats = OSStats()
    os_stats.datetime = tz.localize(yesterday)
    os_stats.os = os[0] + " " + os[1]
    os_stats.page_views = len(os_logs)
    os_stats.save()

for platform in platforms:

    platform_logs = yesterdays_logs.filter(device_type=platform)

    platform_stats = PlatformStats()
    platform_stats.datetime = tz.localize(yesterday)
    platform_stats.platform = platform
    platform_stats.page_views = len(platform_logs)
    platform_stats.save()
        