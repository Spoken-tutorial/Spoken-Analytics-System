"""
This script takes logs from the 'Log' and calculates no of page loads 
from different sources (search, referrer and direct).

The script runs everyday after 12:00 AM.
"""

import datetime
from dashboard.models import Log, SourcesStats
from django.db.models import Count
from pytz import timezone
from django.conf import settings

# Timezone object used to localize time in current timezone
tz = timezone(settings.TIME_ZONE)

yesterday = datetime.datetime.now() - datetime.timedelta(3)

yesterday_min = datetime.datetime.combine(yesterday, datetime.time.min) # Yesterdays min datetime
yesterday_max = datetime.datetime.combine(yesterday, datetime.time.max) # Yesterdays max datetime

# make datetimes timezone aware
yesterday_min = tz.localize(yesterday_min)
yesterday_max = tz.localize(yesterday_max)

yesterdays_logs_count = Log.objects.filter(datetime__range=(yesterday_min, yesterday_max)).count()

total_referring_urls_having_spoken = Log.objects.filter(referrer__icontains='spoken').filter(datetime__range=(yesterday_min, yesterday_max)).count()
total_direct_traffic = Log.objects.filter(referrer__contains='(No referring link)').filter(datetime__range=(yesterday_min, yesterday_max)).count()
total_search_traffic = Log.objects.filter(referrer__icontains='https://www.google.com/').filter(datetime__range=(yesterday_min, yesterday_max)).count()
total_referrer_traffic = yesterdays_logs_count - total_referring_urls_having_spoken - total_direct_traffic - total_search_traffic

sources_stats = SourcesStats()

sources_stats.datetime = tz.localize(yesterday)
sources_stats.direct_page_views = total_direct_traffic
sources_stats.search_page_views = total_search_traffic
sources_stats.referrer_page_views = total_referrer_traffic

sources_stats.save()
