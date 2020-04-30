import json

from django.shortcuts import render
from django.http import HttpResponse
from .models import Log
from django.db.models import Count, Q
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from datetime import date, datetime, timedelta

# Create your views here.
def index(request):
    # This view renders the dashboard page

    return render(request, 'index.html')

# this view serves the data required to plot graph on dashboard
def graphData(request):
    # Getting data
    obj = Log.objects.extra({'timestamp' : "date(timestamp)"}).values('timestamp').annotate(total=Count('id'))
    data = json.dumps(list(obj), cls=DjangoJSONEncoder) # converting data to json
    print(data)
    return JsonResponse(data, safe=False) # sending data