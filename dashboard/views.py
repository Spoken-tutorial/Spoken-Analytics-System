import json

from django.db import connections
from bson.json_util import dumps
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.utils.timezone import get_current_timezone
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Sum
from .models import Log, DailyStats, WeeklyStats, MonthlyStats, YearlyStats, AverageStats, EventStats, FossStats, RegionStats, CityStats

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
    Suppy data to graph for visualization
    """

    data = json.loads(request.body) # Extract data from request

    data_summary_type = data['data_summary_type']

    
    # if data_summary_type is 'weekly' the data object is like
    # {'data_summary_type': 'weekly', 'from': {'week': '15', 'year': '2020'}, 'to': {'week': '19', 'year': '2020'}}
    # else the data object is like
    # {'data_summary_type': 'daily', 'from': '2020-05-01', 'to': '2020-05-08'}

    # Duration of which data is to be sent
    if(data_summary_type == 'weekly'):
        
        from_week = data['from']['week']
        from_year = data['from']['year']

        to_week = data['to']['week']
        to_year = data['to']['year']

        from_week_year = str(from_year) + '-W' + str(from_week) # conveting week and year in the format
        to_week_year = str(to_year) + '-W' + str(to_week)       # 2020-W03 for it to be converted into datetime object

        from_date = datetime.strptime(from_week_year + '-1', '%G-W%V-%u') # converting to datetime object
        to_date = datetime.strptime(to_week_year + '-1', '%G-W%V-%u')     # converting to datetime object

    else:

        from_date = datetime.strptime(data['from'], '%Y-%m-%d') # converting to datetime object
        to_date = datetime.strptime(data['to'], '%Y-%m-%d')     # converting to datetime object

    # extracting data on basis of granuality (weekly, monthly, etc)
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

    # getting average stats
    avg_stats = AverageStats.objects.all()

    # Converting data to json object
    json_avg_stats = serializers.serialize('json', avg_stats)

    json_res = {'stats': json_stats, 'avg_stats': json_avg_stats}

    return JsonResponse(json_res, safe=False) # sending data

def events(request):
    """
    Renders the events page
    """

    today = datetime.today()
    day_before = today - timedelta(days=1)

    # getting event stats of 4 days ago
    # you can choose any day but difference must be of 1 day
    event_stats = EventStats.objects.filter(date__range=(day_before, today)).values('event_name', 'path_info').order_by('event_name').annotate(unique_visits=Sum('unique_visits'))

    context = {
        'event_stats': event_stats,
    }

    return render(request, 'events.html', context)

def eventsData(request):
    """
    Suppy data to data table of events page
    """

    data = json.loads(request.body) # Extract data from request

    from_date = datetime.strptime(data['from'], '%Y-%m-%d') # converting to datetime object
    to_date = datetime.strptime(data['to'], '%Y-%m-%d')     # converting to datetime object

    # getting events stats from database
    event_stats = EventStats.objects.filter(date__range=(from_date, to_date)).values('event_name', 'path_info').order_by('event_name').annotate(unique_visits=Sum('unique_visits'))

    # Converting data to json object
    json_res = json.dumps(list(event_stats), cls=DjangoJSONEncoder)

    return JsonResponse(json_res, safe=False) # sending data

def eventAnalysis(request, event_name):
    """
    Renders the event analysis page
    From users perspective events are 'pages'
    """
    context = {
        'event_name': event_name,
    }
    return render(request, 'event_analysis.html', context)

def eventAnalysisGraphData(request):
    """
    Suppy data to event analysis graph for visualization
    """

    data = json.loads(request.body) # Extract data from request

    event_name = data['event_name']
    from_date = datetime.strptime(data['from'], '%Y-%m-%d') # converting to datetime object
    to_date = datetime.strptime(data['to'], '%Y-%m-%d')     # converting to datetime object

    # getting events stats from database
    event_stats = EventStats.objects.filter(event_name=event_name).filter(date__range=(from_date, to_date)).values('date').order_by('date').annotate(unique_visits=Sum('unique_visits'))

    # Converting data to json object
    json_res = json.dumps(list(event_stats), cls=DjangoJSONEncoder)

    return JsonResponse(json_res, safe=False) # sending data

def reports(request):
    """
    Renders the reports page
    """
    return render(request, 'reports.html')

def getLocationStats(request):
    """
    Suppy data to reports page
    """

    region_stats = RegionStats.objects.all().order_by('-page_views')[0:10]
    city_stats = CityStats.objects.all().order_by('-page_views')[0:10]

    total_page_views = Log.objects.all().count()

    json_region_stats = serializers.serialize('json', region_stats)

    json_city_stats = serializers.serialize('json', city_stats)

    json_res = {'region_stats': json_region_stats, 'city_stats': json_city_stats, 'total_page_views': total_page_views}

    return JsonResponse(json_res, safe=False)

def foss(request):
    """
    Renders the foss page
    """

    today = datetime.today()
    day_before = today - timedelta(days=1)

    # getting foss stats of 1 day
    foss_stats = FossStats.objects.filter(date__range=(day_before, today)).values('foss_name').order_by('foss_name').annotate(unique_visits=Sum('unique_visits'))

    context = {
        'foss_stats': foss_stats,
    }

    return render(request, 'foss.html', context)


def fossData(request):
    """
    Suppy data to data table of reports page
    """

    data = json.loads(request.body) # Extract data from request

    from_date = datetime.strptime(data['from'], '%Y-%m-%d') # converting to datetime object
    to_date = datetime.strptime(data['to'], '%Y-%m-%d')     # converting to datetime object

    # getting foss stats from database
    foss_stats = FossStats.objects.filter(date__range=(from_date, to_date)).values('foss_name').order_by('foss_name').annotate(unique_visits=Sum('unique_visits'))

    # Converting data to json object
    json_res = json.dumps(list(foss_stats), cls=DjangoJSONEncoder)

    return JsonResponse(json_res, safe=False) # sending data