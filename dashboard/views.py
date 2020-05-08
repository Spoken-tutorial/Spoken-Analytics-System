import json

from django.db import connections
from bson.json_util import dumps
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.core import serializers

from .models import Log, DailyStats, WeeklyStats, MonthlyStats, YearlyStats, AverageStats

# Create your views here.
def index(request):
    """
    Renders the dashboard page
    """
    # Fetching data from averagestats collection
    average_stats = AverageStats.objects.all()[0]

    context = {
        'average_stats': average_stats,
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

        from_week_year = str(from_year) + '-W' + str(from_week)
        to_week_year = str(to_year) + '-W' + str(to_week)

        from_date = datetime.strptime(from_week_year + '-1', '%G-W%V-%u')
        to_date = datetime.strptime(to_week_year + '-1', '%G-W%V-%u')
        print(from_date, to_date)

    else:

        from_date = datetime.strptime(data['from'], '%Y-%m-%d')
        to_date = datetime.strptime(data['to'], '%Y-%m-%d')

    if data_summary_type == 'daily':
        
        stats = DailyStats.objects.filter(date__gte=from_date, date__lte=to_date).order_by('date')

    elif data_summary_type == 'weekly':

        stats = WeeklyStats.objects.filter(date__range=(from_date, to_date)).order_by('date')
    
    elif data_summary_type == 'monthly':

        stats = MonthlyStats.objects.filter(date__range=(from_date, to_date)).order_by('date')

    elif data_summary_type == 'yearly':

        stats = YearlyStats.objects.filter(date__range=(from_date, to_date)).order_by('date')

    # Converting data to json object
    json_stats = serializers.serialize('json', stats)

    avg_stats = AverageStats.objects.all()

    json_avg_stats = serializers.serialize('json', avg_stats)

    json_res = {'stats': json_stats, 'avg_stats': json_avg_stats}

    return JsonResponse(json_res, safe=False) # sending data