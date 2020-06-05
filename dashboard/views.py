import json

from django.conf import settings
from django.db import connections
from bson.json_util import dumps
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta, time
from pytz import timezone
from django.core import serializers
from djgeojson.serializers import Serializer as GeoJSONSerializer
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Sum
from .models import Log, DailyStats, WeeklyStats, MonthlyStats, YearlyStats, AverageStats
from .models import EventStats, FossStats, RegionStats, CityStats, CameFromActivity, ExitLinkActivity
from .models import VisitorSpot, PageViewActivity, VisitorActivity, VisitorPath, VisitorInfo
from .models import BrowserStats, PlatformStats, OSStats, SourcesStats, CameFromStats, ExitLinkStats

# get current timezone 
tz = timezone(settings.TIME_ZONE)

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
        
        to_date_max = datetime.combine(to_date, time.max) # max time for to_date
        
        # make datetimes timezone aware
        from_date = tz.localize(from_date)
        to_date = tz.localize(to_date_max)

    # extracting data on basis of granuality (weekly, monthly, etc)
    if data_summary_type == 'daily':
        
        stats = DailyStats.objects.filter(datetime__gte=from_date, datetime__lte=to_date).order_by('datetime')

    elif data_summary_type == 'weekly':

        stats = WeeklyStats.objects.filter(datetime__range=(from_date, to_date)).order_by('datetime')
    
    elif data_summary_type == 'monthly':

        stats = MonthlyStats.objects.filter(datetime__range=(from_date, to_date)).order_by('datetime')

    elif data_summary_type == 'yearly':

        stats = YearlyStats.objects.filter(datetime__range=(from_date, to_date)).order_by('datetime')

    # Converting data to json objectdatetime.
    json_stats = serializers.serialize('json', stats)

    # getting average stats
    avg_stats = AverageStats.objects.all().order_by('-datetime').first()

    # Converting data to json object
    json_avg_stats = serializers.serialize('json', [avg_stats])

    json_res = {'stats': json_stats, 'avg_stats': json_avg_stats}

    return JsonResponse(json_res, safe=False) # sending data

def events(request):
    """
    Renders the events page
    """
    return render(request, 'events.html')

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
    event_stats = EventStats.objects.filter(date__range=(from_date, to_date)).values('path_info', 'page_title').order_by('-unique_visits').annotate(unique_visits=Sum('unique_visits'))

    # Converting data to json objectath_info = models.CharFi
    json_res = json.dumps(list(event_stats), cls=DjangoJSONEncoder)

    return JsonResponse(json_res, safe=False) # sending data

def eventAnalysis(request):
    """
    Renders the event analysis page
    From users perspective events are 'pages'
    """

    # Gettign path from request object
    path = request.GET.get('path', '')

    context = {
        'path': path,
    }
    return render(request, 'event_analysis.html', context)

def eventAnalysisGraphData(request):
    """
    Suppy data to event analysis graph for visualization
    """

    data = json.loads(request.body) # Extract data from request

    path = data['path']
    from_date = datetime.strptime(data['from'], '%Y-%m-%d') # converting to datetime object
    to_date = datetime.strptime(data['to'], '%Y-%m-%d')     # converting to datetime object

    # make datetimes timezone aware
    from_date = tz.localize(from_date)
    to_date = tz.localize(to_date)

    # getting events stats from database
    event_stats = EventStats.objects.filter(path_info=path).filter(date__range=(from_date, to_date)).values('date').order_by('date').annotate(unique_visits=Sum('unique_visits'))
    
    # for stats in event_stats
    
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
    region_stats = RegionStats.objects.values('region').order_by('-page_views').annotate(page_views=Sum('page_views'))[0:10]
    city_stats = CityStats.objects.values('city').order_by('-page_views').annotate(page_views=Sum('page_views'))[0:10]

    foss_stats = FossStats.objects.values('foss_name').order_by('-page_views').annotate(page_views=Sum('page_views'))[0:10]
    events_stats = EventStats.objects.values('path_info', 'page_title').order_by('-page_views').annotate(page_views=Sum('page_views'))[0:10]

    browser_stats = BrowserStats.objects.values('name').order_by('-page_views').annotate(page_views=Sum('page_views'))[0:10]
    platform_stats = PlatformStats.objects.values('platform').order_by('-page_views').annotate(page_views=Sum('page_views'))[0:10]
    os_stats = OSStats.objects.values('os').order_by('-page_views').annotate(page_views=Sum('page_views'))[0:10]
    
    sources_stats = SourcesStats.objects.aggregate(Sum('referrer_page_views'),Sum('search_page_views'),Sum('direct_page_views'))
    came_from_stats = CameFromStats.objects.values('referrer').order_by('-page_views').annotate(page_views=Sum('page_views'))[0:10]
    exit_link_stats = ExitLinkStats.objects.values('exit_link').order_by('-page_views').annotate(page_views=Sum('page_views'))[0:10]

    # total page views (needed to find percentage of page views)
    total_region_stats_page_views = RegionStats.objects.aggregate(Sum('page_views'))
    total_city_stats_page_views = CityStats.objects.aggregate(Sum('page_views'))
    total_foss_page_views = FossStats.objects.aggregate(Sum('page_views'))
    total_events_page_views = EventStats.objects.aggregate(Sum('page_views'))
    total_browser_page_views = BrowserStats.objects.aggregate(Sum('page_views'))
    total_platform_page_views = PlatformStats.objects.aggregate(Sum('page_views'))
    total_os_page_views = OSStats.objects.aggregate(Sum('page_views'))

    # Converting data to json format
    json_region_stats = json.dumps(list(region_stats), cls=DjangoJSONEncoder)
    json_city_stats = json.dumps(list(city_stats), cls=DjangoJSONEncoder)

    json_foss_stats = json.dumps(list(foss_stats), cls=DjangoJSONEncoder)
    json_event_stats = json.dumps(list(events_stats), cls=DjangoJSONEncoder)

    json_browser_stats = json.dumps(list(browser_stats), cls=DjangoJSONEncoder)
    json_platform_stats = json.dumps(list(platform_stats), cls=DjangoJSONEncoder)
    json_os_stats = json.dumps(list(os_stats), cls=DjangoJSONEncoder)

    json_came_from_stats = json.dumps(list(came_from_stats), cls=DjangoJSONEncoder)
    json_exit_link_stats = json.dumps(list(exit_link_stats), cls=DjangoJSONEncoder)

    json_res = {
        'region_stats': json_region_stats,
        'city_stats': json_city_stats,  
        'total_region_stats_page_views': total_region_stats_page_views['page_views__sum'],
        'total_city_stats_page_views': total_city_stats_page_views['page_views__sum'],

        'foss_stats': json_foss_stats,
        'total_foss_page_views': total_foss_page_views['page_views__sum'],
        'events_stats': json_event_stats,
        'total_events_page_views': total_events_page_views['page_views__sum'],

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
    return render(request, 'foss.html')


def fossData(request):
    """
    Suppy data to data table of foss page
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
    region_stats = RegionStats.objects.values('region').order_by('-page_views').annotate(page_views=Sum('page_views'))
    city_stats = CityStats.objects.values('city').order_by('-page_views').annotate(page_views=Sum('page_views'))

    total_region_stats_page_views = RegionStats.objects.aggregate(Sum('page_views'))['page_views__sum']
    total_city_stats_page_views = CityStats.objects.aggregate(Sum('page_views'))['page_views__sum']

    # variables to store stats
    r_stats = []
    c_stats = []

    # Preparing data to be sent to template
    for stat in region_stats:
        r_stats.append({'region' : stat['region'], 'page_views': int(stat['page_views']), 'percentage': round((stat['page_views']/total_region_stats_page_views) * 100, 2)})
    
    for stat in city_stats:
        c_stats.append({'city' : stat['city'], 'page_views': int(stat['page_views']), 'percentage': round((stat['page_views']/total_city_stats_page_views) * 100, 2)})

    context = {
        'region_stats': r_stats,
        'city_stats': c_stats
    }

    return render(request, 'location_report.html', context)

def cameFromActivity(request):
    """
    Renders the came from activity page
    """
    return render(request, 'came_from_activity.html')

def cameFromActivityData(request):
    """
    Suppy data to data table of came from activity page
    """

    data = json.loads(request.body) # Extract data from request
    
    from_datetime = datetime.strptime(data['from'], '%Y-%m-%d %H:%M') # converting to datetime object
    to_datetime = datetime.strptime(data['to'], '%Y-%m-%d %H:%M')     # converting to datetime object

    # make datetimes timezone aware
    from_datetime = tz.localize(from_datetime)
    to_datetime = tz.localize(to_datetime)

    # getting visitor activity stats from database
    came_from_activity_stats = CameFromActivity.objects.filter(datetime__range=(from_datetime, to_datetime))

    # Converting data to json object
    json_res = serializers.serialize('json', came_from_activity_stats)

    return JsonResponse(json_res, safe=False) # sending data


def exitLinkActivity(request):
    """
    Renders the exit link activity page
    """
    return render(request, 'exit_link_activity.html')

def exitLinkActivityData(request):
    """
    Suppy data to data table of exit link activity page
    """

    data = json.loads(request.body) # Extract data from request
    
    from_datetime = datetime.strptime(data['from'], '%Y-%m-%d %H:%M') # converting to datetime object
    to_datetime = datetime.strptime(data['to'], '%Y-%m-%d %H:%M')     # converting to datetime object

    # make datetimes timezone aware
    from_datetime = tz.localize(from_datetime)
    to_datetime = tz.localize(to_datetime)

    # getting visitor activity stats from database
    exit_link_activity_stats = ExitLinkActivity.objects.filter(datetime__range=(from_datetime, to_datetime))

    # Converting data to json object
    json_res = serializers.serialize('json', exit_link_activity_stats)

    return JsonResponse(json_res, safe=False) # sending data


def visitorMap(request):
    """
    Renders the visitor map page
    """
    return render(request, 'visitor_map.html')

def visitorMapData(request):
    """
    Suppy data to data table of exit link activity page
    """

    data = json.loads(request.body) # Extract data from request
    
    from_datetime = datetime.strptime(data['from'], '%Y-%m-%d %H:%M') # converting to datetime object
    to_datetime = datetime.strptime(data['to'], '%Y-%m-%d %H:%M')     # converting to datetime object

    # make datetimes timezone aware
    from_datetime = tz.localize(from_datetime)
    to_datetime = tz.localize(to_datetime)

    # getting visitor spot stats from database
    visitor_spot_stats = VisitorSpot.objects.filter(datetime__range=(from_datetime, to_datetime))

    # Converting data to json object
    json_res = GeoJSONSerializer().serialize(visitor_spot_stats, use_natural_keys=True, with_modelname=False)

    return JsonResponse(json_res, safe=False) # sending data


def pageViewActivity(request):
    """
    Renders the page view activity page
    """
    return render(request, 'page_view_activity.html')

def pageViewActivityData(request):
    """
    Suppy data to data table of page view activity page
    """

    data = json.loads(request.body) # Extract data from request
    
    from_datetime = datetime.strptime(data['from'], '%Y-%m-%d %H:%M') # converting to datetime object
    to_datetime = datetime.strptime(data['to'], '%Y-%m-%d %H:%M')     # converting to datetime object

    # make datetimes timezone aware
    from_datetime = tz.localize(from_datetime)
    to_datetime = tz.localize(to_datetime)

    # getting visitor activity stats from database
    page_view_activity_stats = PageViewActivity.objects.filter(datetime__range=(from_datetime, to_datetime))

    # Converting data to json object
    json_res = serializers.serialize('json', page_view_activity_stats)

    return JsonResponse(json_res, safe=False) # sending data

def visitorActivity(request):
    """
    Renders the visitor activity page
    """
    return render(request, 'visitor_activity.html')


def visitorActivityData(request):
    """
    Suppy data to data table of visitor activity page
    """

    data = json.loads(request.body) # Extract data from request
    
    from_datetime = datetime.strptime(data['from'], '%Y-%m-%d %H:%M') # converting to datetime object
    to_datetime = datetime.strptime(data['to'], '%Y-%m-%d %H:%M')     # converting to datetime object

    # make datetimes timezone aware
    from_datetime = tz.localize(from_datetime)
    to_datetime = tz.localize(to_datetime)

    # getting visitor activity stats from database
    visitor_activity_stats = VisitorActivity.objects.filter(datetime__range=(from_datetime, to_datetime))

    # Converting data to json object
    json_res = serializers.serialize('json', visitor_activity_stats)

    return JsonResponse(json_res, safe=False) # sending data

def visitorPath(request):
    """
    Renders the visitor paths page
    """
    return render(request, 'visitor_paths.html')

def visitorPathData(request):
    """
    Suppy data to data table of visitor path page
    """

    data = json.loads(request.body) # Extract data from request
    
    from_datetime = datetime.strptime(data['from'], '%Y-%m-%d %H:%M') # converting to datetime object
    to_datetime = datetime.strptime(data['to'], '%Y-%m-%d %H:%M')     # converting to datetime object

    # make datetimes timezone aware
    from_datetime = tz.localize(from_datetime)
    to_datetime = tz.localize(to_datetime)

    # getting visitor path stats from database
    visitor_path_stats = VisitorPath.objects.filter(datetime__range=(from_datetime, to_datetime))

    # Converting data to json object
    json_res = serializers.serialize('json', visitor_path_stats)

    return JsonResponse(json_res, safe=False) # sending data

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
    event_stats = EventStats.objects.values('page_title').order_by('-page_views').annotate(page_views=Sum('page_views'))

    total_foss_page_views = FossStats.objects.aggregate(Sum('page_views'))['page_views__sum']
    total_events_page_views = EventStats.objects.aggregate(Sum('page_views'))['page_views__sum']

    # variables to store stats
    e_stats = []
    f_stats = []

    # Preparing data to be sent to template
    for stat in event_stats:
        e_stats.append({'page_title' : stat['page_title'], 'page_views': int(stat['page_views']), 'percentage': round((stat['page_views']/total_events_page_views) * 100, 2)})
    
    for stat in foss_stats:
        f_stats.append({'foss_name' : stat['foss_name'], 'page_views': int(stat['page_views']), 'percentage': round((stat['page_views']/total_foss_page_views) * 100, 2)})

    context = {
        'foss_stats': f_stats,
        'event_stats': e_stats,
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
    came_from_stats = CameFromStats.objects.values('referrer').order_by('-page_views').annotate(page_views=Sum('page_views'))
    exit_link_stats = ExitLinkStats.objects.values('exit_link').order_by('-page_views').annotate(page_views=Sum('page_views'))


    context = {
        'came_from_stats': came_from_stats,
        'exit_link_stats': exit_link_stats,
    }

    return render(request, 'traffic_report.html', context)



"""
Views of features to be implemented in next version
"""
# def downloadActivity(request):
#     """
#     Renders the download activity page
#     """

#     # retrieving data from database
#     obj = DownloadActivity.objects.all().order_by('-datetime')[0:150]

#     context = {
#         'download_activity': obj
#     }
    
#     return render(request, 'download_activity.html', context)

# def keywordActivity(request):
#     """
#     Renders the keyword activity page
#     """

#     # retriving data from database
#     obj = KeywordActivity.objects.all().order_by('-datetime')[0:25]

#     context = {
#         'keyword_activity': obj,
#     }
    
#     return render(request, 'keyword_activity.html', context)