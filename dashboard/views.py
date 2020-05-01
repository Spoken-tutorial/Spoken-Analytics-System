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
    return render(request, 'index.html')

# This view serves the data required to plot graph on dashboard
def graphData(request):
    """
    Suppy data to graph to display page loads per day
    """
    fromdate = datetime.strptime(request.GET['fromDate'], '%Y-%m-%d')
    todate = datetime.strptime(request.GET['toDate'], '%Y-%m-%d')

    # building mongo query
    q = [{"$match": {"datetime": { "$gte": fromdate, "$lte": todate }}}
    , {'$group': {'_id': {'date': { '$dateToString': {'date': '$datetime', 'format' : '%Y-%m-%d'}}}
    , 'count': { '$sum': 1 }}}, {'$sort': { '_id.date': 1 }}]

    obj = Log.objects.mongo_aggregate(q)
    qs_json = dumps(obj)
    return JsonResponse(qs_json, safe=False) # sending data