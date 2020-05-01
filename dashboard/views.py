import json

from django.db import connections
from bson.json_util import dumps
from django.shortcuts import render
from .models import Log
from django.http import JsonResponse
from datetime import datetime

# Create your views here.
def index(request):
    """
    Renders the dashboard page
    """

    total_page_views = Log.objects.mongo_count()
    max_date = Log.objects.all().order_by('-datetime')[0].datetime
    min_date = Log.objects.all().order_by('datetime')[0].datetime
    time_diff = max_date - min_date
    average_daily_page_views = int(total_page_views / time_diff.days)

    context = {
        'average_daily_page_views': average_daily_page_views
    }
    return render(request, 'index.html', context)

# This view serves the data required to plot graph on dashboard
def graphData(request):
    """
    Suppy data to graph to display page loads per day
    """
    from_date = datetime.strptime(request.GET['fromDate'], '%Y-%m-%d')
    to_date = datetime.strptime(request.GET['toDate'], '%Y-%m-%d')

    # building mongo query
    q = [{"$match": {"datetime": { "$gte": from_date, "$lte": to_date }}}
    , {'$group': {'_id': {'date': { '$dateToString': {'date': '$datetime', 'format' : '%Y-%m-%d'}}}
    , 'count': { '$sum': 1 }}}, {'$sort': { '_id.date': 1 }}]

    obj = Log.objects.mongo_aggregate(q)
    qs_json = dumps(obj)
    return JsonResponse(qs_json, safe=False) # sending data