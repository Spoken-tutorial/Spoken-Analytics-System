import json

from django.db import connections
from django.db.models import Avg
from bson.json_util import dumps
from django.shortcuts import render
from .models import Log, DailyStats
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.core import serializers

# Create your views here.
def index(request):
    """
    Renders the dashboard page
    """
    # Fetching data from dashboard_dailystats collection
    daily_stats = DailyStats.objects.all() 

    # Variables to store stats
    num_days = 0
    total_page_views = 0
    total_unique_visits = 0
    total_first_time_visits = 0
    total_returning_visits = 0

    # Calculating stats
    for stats in daily_stats:
        num_days += 1
        total_page_views += stats.page_views
        total_unique_visits += stats.unique_visits
        total_first_time_visits += stats.first_time_visits
        total_returning_visits += stats.returning_visits
    

    average_daily_page_views = int(total_page_views/num_days)
    average_daily_unique_visits = int(total_unique_visits/num_days)
    average_daily_first_time_visits = int(total_first_time_visits/num_days)
    average_daily_returning_visits = int(total_returning_visits/num_days)


    context = {
        'average_daily_page_views': average_daily_page_views,
        'average_daily_unique_visits': average_daily_unique_visits,
        'average_daily_first_time_visits': average_daily_first_time_visits,
        'average_daily_returning_visits': average_daily_returning_visits,
    }
    
    return render(request, 'index.html', context)

# This view serves the daily stats to graph of dashboard
def graphData(request):
    """
    Suppy data to graph to display page loads per day
    """

    data = json.loads(request.body) # Fetch data from request

    # Duration of which data is to send
    from_date = datetime.strptime(data['fromDate'], '%Y-%m-%d')
    to_date = datetime.strptime(data['toDate'], '%Y-%m-%d') + timedelta(days=1)

    # Extracting data from database
    daily_stats = DailyStats.objects.filter(date__gte=from_date, date__lte=to_date).order_by('date')

    # Converting data to json object
    json_res = serializers.serialize('json', list(daily_stats))

    return JsonResponse(json_res, safe=False) # sending data

# This view serves the weekly stats to graph of dashboard
# def weeklyGraphData():

#     data = json.loads(request.body) # Fetch data from request

#     # Duration of which data is to send
#     from_week = datetime.strptime(data['fromWeek'], '%Y-%m-%d')
#     to_week = datetime.strptime(data['toWeek'], '%Y-%m-%d') + timedelta(days=1)

#     # Extracting data from database
#     daily_stats = DailyStats.objects.filter(date__gte=from_date, date__lte=to_date).order_by('date')

#     # Converting data to json object
#     json_res = serializers.serialize('json', list(daily_stats))

#     return JsonResponse({}, safe=False) # sending data