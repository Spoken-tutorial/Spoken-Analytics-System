import json

from django.db import connections
from django.db.models import Avg
from bson.json_util import dumps
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.core import serializers

from .models import Log, DailyStats, WeeklyStats, MonthlyStats, YearlyStats

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

    data_summary_type = data['data_summary_type']

    # Duration of which data is to send

    if(data_summary_type == 'weekly'):
        
        from_week = data['from']['week']
        from_year = data['from']['year']

        to_week = data['to']['week']
        to_year = data['to']['year']

    else:

        from_date = datetime.strptime(data['from'], '%Y-%m-%d')
        to_date = datetime.strptime(data['to'], '%Y-%m-%d')

    if data_summary_type == 'daily':
        
        stats = DailyStats.objects.filter(date__gte=from_date, date__lte=to_date).order_by('date')

    elif data_summary_type == 'weekly':

        stats = WeeklyStats.objects.filter(year__gte=from_year, year__lte=to_year, week_of_year__gte=from_week, week_of_year__lte=to_week).order_by('year', 'week_of_year')
    
    elif data_summary_type == 'monthly':

        stats = MonthlyStats.objects.filter(month_of_year__gte=from_date.month, month_of_year__lte=to_date.month, year__gte=from_date.year, year__lte=to_date.year).order_by('year', 'month_of_year')

    elif data_summary_type == 'yearly':

        stats = YearlyStats.objects.filter(year__gte=from_date.year, year__lte=to_date.year).order_by('year')
        
    
    # Converting data to json object
    json_res = serializers.serialize('json', list(stats))
    return JsonResponse(json_res, safe=False) # sending data