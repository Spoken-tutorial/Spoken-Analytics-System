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

    # calculating average daily page views
    # total_page_views = Log.objects.mongo_count()
    # max_date = Log.objects.all().order_by('-datetime')[0].datetime
    # min_date = Log.objects.all().order_by('datetime')[0].datetime
    # time_diff = max_date - min_date
    # average_daily_page_views = int(total_page_views / time_diff.days)

    # Calculating average daily unique visits
    # number_of_distinct_ip_addresses = len(Log.objects.mongo_distinct('ip_address'))
    # average_daily_unique_visits = int(number_of_distinct_ip_addresses / time_diff.days)

    # Calculating average daily first time visits
    # total_first_time_visits = Log.objects.filter(first_time_visit="True").count()
    # average_daily_first_time_visits = int(total_first_time_visits / time_diff.days)

    # Calculating average daily returning visits
    # total_returning_visits = Log.objects.filter(first_time_visit="True").count()
    # average_daily_returning_visits = int(total_returning_visits / time_diff.days)

    daily_stats = DailyStats.objects.all()

    num_days = 0
    total_page_views = 0
    total_unique_visits = 0
    total_first_time_visits = 0
    total_returning_visits = 0


    for stats in daily_stats:
        num_days += 1
        total_page_views += stats.page_loads
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

# This view serves the data required to plot graph on dashboard
def graphData(request):
    """
    Suppy data to graph to display page loads per day
    """

    data = json.loads(request.body)

    from_date = datetime.strptime(data['fromDate'], '%Y-%m-%d')
    to_date = datetime.strptime(data['toDate'], '%Y-%m-%d') + timedelta(days=1)

    # # query to get daily page loads
    # query_daily_page_loads = [{"$match": {"datetime": { "$gte": from_date, "$lte": to_date }}}
    # , {'$group': {'_id': {'date': { '$dateToString': {'date': '$datetime', 'format' : '%Y-%m-%d'}}}
    # , 'count': { '$sum': 1 }}}, {'$sort': { '_id.date': 1 }}]


    # daily_page_loads_obj = Log.objects.mongo_aggregate(query_daily_page_loads)
    # daily_page_loads_json = dumps(daily_page_loads_obj)

    # # query to get daily unique visits
    # query_daily_unique_visits = [{'$match': {'datetime': { '$gte': from_date, '$lte': to_date }}}
    # , {'$group': {'_id': {'date': { '$dateToString': {'date': '$datetime', 'format' : '%Y-%m-%d'}}, 'ip_address': '$ip_address'}}}
    # , {'$group': {'_id': {'date': '$_id.date'} ,'count': {'$sum': 1}}}
    # , {'$sort': { '_id.date': 1 }}]

    # daily_unique_visits_obj = Log.objects.mongo_aggregate(query_daily_unique_visits)
    # daily_unique_visits_json = dumps(daily_unique_visits_obj)

    # # query to get daily returning visits
    # query_daily_returning_visits = [{'$match': {'datetime': { '$gte': from_date, '$lte': to_date }}}
    # , {'$match': {'first_time_visit': 'False'}}
    # , {'$group': {'_id': {'date': { '$dateToString': {'date': '$datetime', 'format' : '%Y-%m-%d'}}, 'ip_address': '$ip_address'}}}
    #    , {'$group': {'_id': {'date': '$_id.date'} ,'count': {'$sum': 1}}}
    # , {'$sort': { '_id.date': 1 }}]

    # daily_returning_visits_obj = Log.objects.mongo_aggregate(query_daily_returning_visits)
    # daily_returning_visits_json = dumps(daily_returning_visits_obj)

    daily_stats = DailyStats.objects.filter(date__gte=from_date, date__lte=to_date).order_by('date')

    json_res = serializers.serialize('json', list(daily_stats))

    return JsonResponse(json_res, safe=False) # sending data