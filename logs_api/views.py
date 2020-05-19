import redis
import datetime
import json 
import math

from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .utils import update_tutorial_progress


# configurations for redis
redis_client = redis.Redis(
    host = 'localhost',
    port = 6379,
    db = 0
)

@csrf_exempt
def save_website_log (request):

    if request.method != "POST":
        return HttpResponse("You are not allowed to make that request to this page.")

    try:
        data = {}
        data['referer'] = request.POST.get('referer')
        data['browser_name'] = request.POST.get('browser_name')
        data['browser_version'] = request.POST.get('browser_version')
        data['os_name'] = request.POST.get('os_name')
        data['os_version'] = request.POST.get('os_version')
        data['platform'] = request.POST.get('platform')
        data['vendor'] = request.POST.get('vendor')

        # data['event_name'] = EVENT_NAME_DICT[key]['name']
        data['url_name'] = request.POST.get('url_name')
        data['visited_by'] = request.POST.get('visited_by')  # request.user.username if request.user.is_authenticated else 'anonymous'
        data["method"] = request.POST.get('method')
        data['ip_address'] = request.POST.get('ip_address')  # request.META['REMOTE_ADDR']
        data['method'] = request.POST.get ('method')  # request.method
        data['datetime'] = str(datetime.datetime.fromtimestamp(int (request.POST.get("datetime"))/1000))
        data['first_time_visit'] = request.POST.get ('first_time_visit')
        data['country'] = request.POST.get ('country')
        data['region'] = request.POST.get ('region')
        data['city'] = request.POST.get ('city')
        data['latitude'] = request.POST.get ('latitude')
        data['longitude'] = request.POST.get ('longitude')
        # enqueue job in the redis queue named 'tasks3'
        redis_client.rpush('tasks3', json.dumps(data))

    except Exception as e:
        print("Log Exception " + str(e))
    
    return HttpResponse(status=200)


# Create and configure the pymongo client
from pymongo import MongoClient
MONGO_CLIENT = MongoClient()


# TODO: don't let users make their own post requests to this view. Remove CSRF exempt
@csrf_exempt
def save_tutorial_progress (request):

    if request.method != "POST":
        return HttpResponse("You are not allowed to make that request to this page.")

    data = {}
    data['username'] = request.POST.get("username")
    # data['foss'] = request.POST.get("foss")
    # data['foss_lang'] = request.POST.get("foss_lang")
    # data['tutorial'] = request.POST.get("tutorial")
    data['foss_id'] = request.POST.get("foss_id")
    data['tutorial_id'] = request.POST.get("tutorial_id")
    data['language_id'] = request.POST.get("language_id")
    data['curr_time'] = int (request.POST.get("curr_time"))
    data['total_time'] = int (request.POST.get("total_time"))

    # sometimes, on the first video play,
    # this duration is returned as 0 by video.js
    if (data['total_time'] == 0):
        data['total_time'] = math.inf

    data['language_visit_count'] = int (request.POST.get("language_visit_count"))
    data['datetime'] = datetime.datetime.fromtimestamp(int (request.POST.get("timestamp"))/1000)

    update_tutorial_progress (data)  # synchronous call

    return HttpResponse(status=200)

# TODO: don't let users make their own post requests to this view. Remove CSRF exempt
@csrf_exempt
def change_completion (request):

    if request.method != "POST":
        return HttpResponse("You are not allowed to make that request to this page.")

    # configurations for pymongo
    db = MONGO_CLIENT.logs
    tutorial_progress_logs = db.tutorial_progress_logs

    # store in MongoDB
    try:
        
        completed = False
        if request.POST.get("completed") == "true":
            completed = True

        # TODO: don't allow dots in the FOSS names and tutorial names
        completed_field = 'fosses.' + str(request.POST.get('foss_id')) + '.' + str(request.POST.get('language_id')) + '.' + str(request.POST.get('tutorial_id')) + '.completed'
        tutorial_progress_logs.find_one_and_update(
                { "username" : request.POST.get('username') }, 
                { "$set" : { completed_field: completed } },
                upsert=True
        )

        return HttpResponse(status=200)

    except Exception as e:
        print (str(e))
        return HttpResponse(status=500)


# TODO: don't let users make their own post requests to this view. Remove CSRF exempt
@csrf_exempt
def check_completion (request):

    if request.method != "POST":
        return HttpResponse("You are not allowed to make that request to this page.")

    # configurations for pymongo
    db = MONGO_CLIENT.logs
    tutorial_progress_logs = db.tutorial_progress_logs

    try:

        res = tutorial_progress_logs.find_one(
            { "username" : request.POST.get('username') }
        )

        if res['fosses'][str(request.POST.get('foss_id'))][str(request.POST.get('language_id'))][str(request.POST.get('tutorial_id'))]['completed'] == True:
            return HttpResponse(status=200)

        return HttpResponse(status=500)

    except Exception as e:
        print (str(e))
        return HttpResponse(status=500)