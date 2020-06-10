"""
This script stores the location (latitude and longitude) of users in 'VisitorSpot'.
'VisitorSpot' is used to display location of users on Map.

The script runs everyday after 12:05 AM.
"""

import datetime
from dashboard.models import Log, VisitorSpot
from pytz import timezone
from django.conf import settings
from celery import shared_task

@shared_task(bind=True)
def visitor_spot_statistics(self):
    
    # Timezone object used to localize time in current timezone
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
            
    for ip_address in ip_addresses:

        ip_logs = Log.objects.filter(ip_address=ip_address).filter(datetime__range=(yesterday_min, yesterday_max)).order_by('-datetime').first()

        visitor_spot = VisitorSpot()
        visitor_spot.datetime = ip_logs.datetime
        visitor_spot.ip_address =  ip_logs.ip_address
        # geom object is used to display point on graph
        visitor_spot.geom = {'type': 'Point','coordinates': [ip_logs.longitude, ip_logs.latitude] } 
        visitor_spot.save()