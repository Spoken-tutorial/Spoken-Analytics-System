import json

from django.conf import settings
from django.db import connections
from bson.json_util import dumps
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
from pytz import timezone
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Sum
from .models import Log, DailyStats, WeeklyStats, MonthlyStats, YearlyStats, AverageStats
from .models import EventStats, FossStats, RegionStats, CityStats, CameFromActivity, DownloadActivity, ExitLinkActivity
from .models import VisitorSpot, PageViewActivity, VisitorActivity, VisitorPath, KeywordActivity, VisitorInfo
from .models import BrowserStats, PlatformStats, OSStats, SourcesStats, CameFromStats, ExitLinkStats

# get current timezone 
tz = timezone(settings.TIME_ZONE)

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

    # make datetimes timezone aware
    from_date = tz.localize(from_date)
    to_date = tz.localize(to_date)

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
    day_before = today - timedelta(days=2)

    # make datetimes timezone aware
    today = tz.localize(today)
    day_before = tz.localize(day_before)

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
    
    # make datetimes timezone aware
    from_date = tz.localize(from_date)
    to_date = tz.localize(to_date)
    
    # getting events stats from database
    event_stats = EventStats.objects.filter(date__range=(from_date, to_date)).values('event_name', 'path_info').order_by('-unique_visits').annotate(unique_visits=Sum('unique_visits'))

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

    # make datetimes timezone aware
    from_date = tz.localize(from_date)
    to_date = tz.localize(to_date)

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

def getReportsStats(request):
    """
    Suppy data to reports page
    """

    # Getting data from various tables
    region_stats = RegionStats.objects.all().order_by('-page_views')[0:10]
    city_stats = CityStats.objects.all().order_by('-page_views')[0:10]

    foss_stats = FossStats.objects.values('foss_name').order_by('-page_views').annotate(page_views=Sum('page_views'))[0:10]
    # events_stats = EventStats.objects.values('event_name').order_by('-page_views').annotate(page_views=Sum('page_views'))[0:10]

    browser_stats = BrowserStats.objects.values('browser_type').order_by('-page_views').annotate(page_views=Sum('page_views'))[0:10]
    platform_stats = PlatformStats.objects.values('platform').order_by('-page_views').annotate(page_views=Sum('page_views'))[0:10]
    os_stats = OSStats.objects.values('os').order_by('-page_views').annotate(page_views=Sum('page_views'))[0:10]
    
    sources_stats = SourcesStats.objects.aggregate(Sum('referrer_page_views'),Sum('search_page_views'),Sum('direct_page_views'))
    came_from_stats = CameFromStats.objects.values('referrer').order_by('-page_views').annotate(page_views=Sum('page_views'))[0:10]
    exit_link_stats = ExitLinkStats.objects.values('exit_link').order_by('-page_views').annotate(page_views=Sum('page_views'))[0:10]

    # total page views (needed to find percentage of page views)
    total_page_views = Log.objects.all().count()
    total_foss_page_views = FossStats.objects.aggregate(Sum('page_views'))
    # total_events_page_views = EventStats.objects.aggregate(Sum('page_views'))
    total_browser_page_views = BrowserStats.objects.aggregate(Sum('page_views'))
    total_platform_page_views = PlatformStats.objects.aggregate(Sum('page_views'))
    total_os_page_views = OSStats.objects.aggregate(Sum('page_views'))

    # Converting data to json format
    json_region_stats = serializers.serialize('json', region_stats)
    json_city_stats = serializers.serialize('json', city_stats)

    json_foss_stats = json.dumps(list(foss_stats), cls=DjangoJSONEncoder)
    # json_event_stats = json.dumps(list(events_stats), cls=DjangoJSONEncoder)

    json_browser_stats = json.dumps(list(browser_stats), cls=DjangoJSONEncoder)
    json_platform_stats = json.dumps(list(platform_stats), cls=DjangoJSONEncoder)
    json_os_stats = json.dumps(list(os_stats), cls=DjangoJSONEncoder)

    json_came_from_stats = json.dumps(list(came_from_stats), cls=DjangoJSONEncoder)
    json_exit_link_stats = json.dumps(list(exit_link_stats), cls=DjangoJSONEncoder)

    json_res = {
        'region_stats': json_region_stats,
        'city_stats': json_city_stats,  
        'total_page_views': total_page_views,

        'foss_stats': json_foss_stats,
        'total_foss_page_views': total_foss_page_views['page_views__sum'],
        # 'events_stats': json_event_stats,
        # 'total_events_page_views': total_events_page_views['page_views__sum'],

        'browser_stats': json_browser_stats,
        'total_browser_page_views': total_browser_page_views['page_views__sum'],
        'platform_stats': json_platform_stats,
        'total_platform_page_views': total_platform_page_views['page_views__sum'],
        'os_stats': json_os_stats,
        'total_os_page_views': total_os_page_views['page_views__sum'],

        'sources_stats': sources_stats,
        'came_from_stats': json_came_from_stats,
        'exit_link_stats': json_exit_link_stats,
    }

    return JsonResponse(json_res, safe=False) # sending data

def foss(request):
    """
    Renders the foss page
    """

    today = datetime.today()
    day_before = today - timedelta(days=2)
    
    # make datetimes timezone aware
    today = tz.localize(today)
    day_before = tz.localize(day_before)

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

    # make datetimes timezone aware
    from_date = tz.localize(from_date)
    to_date = tz.localize(to_date)

    # getting foss stats from database
    foss_stats = FossStats.objects.filter(date__range=(from_date, to_date)).values('foss_name').order_by('foss_name').annotate(unique_visits=Sum('unique_visits'))

    # Converting data to json object
    json_res = json.dumps(list(foss_stats), cls=DjangoJSONEncoder)

    return JsonResponse(json_res, safe=False) # sending data

def locationReport(request):
    """
    Renders the location stats page
    """
    # Getting data from various tables
    region_stats = RegionStats.objects.all().order_by('-page_views')
    city_stats = CityStats.objects.all().order_by('-page_views')

    total_page_views = Log.objects.all().count()

    # variables to store stats
    r_stats = []
    c_stats = []

    # Preparing data to be sent to template
    for stat in region_stats:
        r_stats.append({'region' : stat.region, 'page_views': int(stat.page_views), 'percentage': round((stat.page_views/total_page_views) * 100, 2)})
    
    for stat in city_stats:
        c_stats.append({'city' : stat.city, 'page_views': int(stat.page_views), 'percentage': round((stat.page_views/total_page_views) * 100, 2)})

    context = {
        'region_stats': r_stats,
        'city_stats': c_stats
    }

    return render(request, 'location_report.html', context)

def cameFromActivity(request):
    """
    Renders the came from activity page
    """

    # retrieving data from database
    obj = CameFromActivity.objects.all().order_by('-datetime')[0:150]

    context = {
        'came_from_activity': obj
    }
    
    return render(request, 'came_from_activity.html', context)

def downloadActivity(request):
    """
    Renders the download activity page
    """

    # retrieving data from database
    obj = DownloadActivity.objects.all().order_by('-datetime')[0:150]

    context = {
        'download_activity': obj
    }
    
    return render(request, 'download_activity.html', context)

def exitLinkActivity(request):
    """
    Renders the exit link activity page
    """

    # retrieving data from database
    obj = ExitLinkActivity.objects.all().order_by('-datetime')[0:150]

    context = {
        'exit_link_activity': obj
    }
    
    return render(request, 'exit_link_activity.html', context)

def visitorMap(request):
    """
    Renders the visitor map page
    """

    # retriving data from database
    obj = VisitorSpot.objects.all().order_by('-datetime')[0:10]

    context = {
        'visitor_spots': obj,
    }
    
    return render(request, 'visitor_map.html', context)

def pageViewActivity(request):
    """
    Renders the page view activity page
    """

    # retriving data from database
    obj = PageViewActivity.objects.all().order_by('-datetime')[0:25]

    context = {
        'page_view_activity': obj,
    }
    
    return render(request, 'page_view_activity.html', context)

def visitorActivity(request):
    """
    Renders the visitor activity page
    """

    # retriving data from database
    obj = VisitorActivity.objects.all().order_by('-latest_page_view')[0:25]

    context = {
        'visitor_activity': obj,
    }
    
    return render(request, 'visitor_activity.html', context)

def visitorPath(request):
    """
    Renders the visitor paths page
    """

    # retriving data from database
    obj = VisitorPath.objects.all().order_by('-datetime')[0:25]

    context = {
        'visitor_path': obj,
    }
    
    return render(request, 'visitor_paths.html', context)

def keywordActivity(request):
    """
    Renders the keyword activity page
    """

    # retriving data from database
    obj = KeywordActivity.objects.all().order_by('-datetime')[0:25]

    context = {
        'keyword_activity': obj,
    }
    
    return render(request, 'keyword_activity.html', context)

def magnify(request):
    """
    Renders the magnify page
    """

    # Gettign IP address from request object
    ip = request.GET.get('ip', '')

    # If ip address was provided find its info else set it to "unavailabel"
    if ip == '':
        visitor_info = "unavailable"
    else:
        visitor_info = VisitorInfo.objects.order_by('-datetime').filter(ip_address=ip).first()

        if visitor_info == None:
            visitor_info = "unavailable"

    context = {
        'ip_address': ip,
        'visitor_info': visitor_info
    }
    
    return render(request, 'magnify.html', context)

def fossEventReport(request):
    """
    Renders the Foss Event Report page
    """

    # Getting data from various tables
    foss_stats = FossStats.objects.values('foss_name').order_by('-page_views').annotate(page_views=Sum('page_views'))
    event_stats = EventStats.objects.values('event_name').order_by('-page_views').annotate(page_views=Sum('page_views'))

    context = {
        'foss_stats': foss_stats,
        'event_stats': event_stats,
    }

    return render(request, 'foss_event_report.html', context)

def systemReport(request):
    """
    Renders the System Report page
    """

    # Getting data from various tables
    browser_stats = BrowserStats.objects.values('name').order_by('-page_views').annotate(page_views=Sum('page_views'))
    platform_stats = PlatformStats.objects.values('platform').order_by('-page_views').annotate(page_views=Sum('page_views'))
    os_stats = OSStats.objects.values('os').order_by('-page_views').annotate(page_views=Sum('page_views'))
    
    total_browser_page_views = BrowserStats.objects.aggregate(Sum('page_views'))['page_views__sum']
    total_platform_page_views = PlatformStats.objects.aggregate(Sum('page_views'))['page_views__sum']
    total_os_page_views = OSStats.objects.aggregate(Sum('page_views'))['page_views__sum']

    # variables to store stats
    b_stats = []
    p_stats = []
    o_stats = []

    # Preparing data to be sent to template
    for stat in browser_stats:
        b_stats.append({'name' : stat['name'], 'page_views': int(stat['page_views']), 'percentage': round((stat['page_views']/total_browser_page_views) * 100, 2)})
    
    for stat in platform_stats:
        p_stats.append({'platform' : stat['platform'], 'page_views': int(stat['page_views']), 'percentage': round((stat['page_views']/total_platform_page_views) * 100, 2)})

    for stat in os_stats:
        o_stats.append({'os' : stat['os'], 'page_views': int(stat['page_views']), 'percentage': round((stat['page_views']/total_os_page_views) * 100, 2)})

    context = {
        'browser_stats': b_stats,
        'platform_stats': p_stats,
        'os_stats': o_stats,
    }

    return render(request, 'system_report.html', context)

def trafficReport(request):
    """
    Renders the Traffic Report page
    """

    # Getting data from various tables
    came_from_stats = CameFromStats.objects.values('referrer').order_by('-page_views').annotate(page_views=Sum('page_views'))[0:10]
    exit_link_stats = ExitLinkStats.objects.values('exit_link').order_by('-page_views').annotate(page_views=Sum('page_views'))[0:10]


    context = {
        'came_from_stats': came_from_stats,
        'exit_link_stats': exit_link_stats,
    }

    return render(request, 'traffic_report.html', context)