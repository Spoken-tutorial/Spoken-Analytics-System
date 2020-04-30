import json

from django.shortcuts import render
from django.http import HttpResponse
from .models import Log
from django.db.models import Count, Q
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from datetime import date, datetime, timedelta

# Create your views here.
def index(request):
    # This view renders the dashboard page
    return render(request, 'index.html')

# This view serves the data required to plot graph on dashboard
def graphData(request):
    # Getting data
    obj = Log.objects.extra({'datetime' : "date(datetime)"}).values('datetime').annotate(total=Count('id'))
    # obj = Log.objects.filter(path_info='main')
    print(obj[0].datetime)
    # qs_json = serializers.serialize('json', obj)
    return JsonResponse('d', safe=False) # sending data