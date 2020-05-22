"""
This script takes logs from the dashboard_log collection, calculates no of page loads from different isps.
"""
import datetime
from dashboard.models import Log, ISPStats
from django.db.models import Count

isp_stats = Log.objects.values('isp').order_by('isp').annotate(count=Count('isp'))

for stats in isp_stats:
    isp_stats = ISPStats()
    isp_stats.isp = stats['isp']
    isp_stats.page_views = stats['count']
    isp_stats.save()
