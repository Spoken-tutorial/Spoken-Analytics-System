import redis
import datetime
import json 
import math
import re

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST   
from .utils import update_tutorial_progress

from analytics_system import MONGO_CLIENT, REDIS_CLIENT, GEOIP2_CLIENT


REGION_CODE_TO_REGION = {
    "AP": "Andhra Pradesh",
    "AR": "Arunachal Pradesh",
    "AS": "Assam",
    "BR": "Bihar",
    "CT": "Chhattisgarh",
    "GA": "Goa",
    "GJ": "Gujarat",
    "HR": "Haryana",
    "HP": "Himachal Pradesh",
    "JK": "Jammu and Kashmir",
    "JH": "Jharkhand",
    "KA": "Karnataka",
    "KL": "Kerala",
    "MP": "Madhya Pradesh",
    "MH": "Maharashtra",
    "MN": "Manipur",
    "ML": "Meghalaya",
    "MZ": "Mizoram",
    "NL": "Nagaland",
    "OR": "Odisha",
    "PB": "Punjab",
    "RJ": "Rajasthan",
    "SK": "Sikkim",
    "TN": "Tamil Nadu",
    "TG": "Telangana",
    "TR": "Tripura",
    "UP": "Uttar Pradesh",
    "UT": "Uttarakhand",
    "WB": "West Bengal",
    "AN": "Andaman and Nicobar Islands",
    "CH": "Chandigarh",
    "DD": "Dadra and Nagar Haveli and Daman and Diu",
    "LA": "Ladakh",
    "LD": "Lakshadweep",
    "DL": "Delhi",
    "PY": "Puducherry",
}

"""
Function called indirectly from the middleware for extracting Geolocation info,
and pushing the log to a redis queue.
"""
@csrf_exempt
@require_POST
def save_middleware_log (request):

    # data = dict(request.POST)
    # print ('\n\n')
    # print (data)
    # print ('\n\n')

    data = {}
    # Note that request.POST can contain multiple items for each key. 
    # If you are expecting multiple items for each key, you can use lists, 
    # which returns all values as a list.
    for key, values in request.POST.lists():

        if key == 'request':
            continue

        if len(values) == 1:
            data[key] = values[0]
        else:
            data[key] = values
    
    if not data['referer']:
        data['referer'] = '(No referring link)'

    # data = {}
    # data['ip_address'] = request.POST.get('ip_address')
    # data['path_info'] = request.POST.get('path_info')
    # data['browser_info'] = request.POST.get('browser_info')
    # data['event_name'] = request.POST.get('event_name')
    # data['visited_by'] = request.POST.get('visited_by')
    # data['ip_address'] = request.POST.get('ip_address')
    # data['view_args'] = request.POST.get('view_args')
    # data['view_kwargs'] = request.POST.get('view_kwargs')
    # data['body'] = request.POST.get('body')
    # data['method'] = request.POST.get('method')
    # data['datetime'] = request.POST.get('datetime')
    # data['referer'] = request.POST.get('referer')
    # data['browser_family'] = request.POST.get('browser_family')
    # data['browser_version'] = request.POST.get('browser_version')
    # data['os_family'] = request.POST.get('os_family')
    # data['os_version'] = request.POST.get('os_version')
    # data['device_family'] = request.POST.get('device_family')
    # data['device_type'] = request.POST.get('device_type')
    # data['first_time_visit'] = request.POST.get ('first_time_visit')

    # if request.POST.get ('post_data'):
    #     data['post_data'] = request.POST.get ('post_data')

    try:

        # if the address is not a properly formatted IPv4 or IPv6, reject the log
        if not re.match(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', data["ip_address"]):
            if not re.match(r'^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$', data['ip_address']):
                return
        
        # extract Geolocation info
        try:
            location = GEOIP2_CLIENT.city(data['ip_address'])
            data["latitude"] = location["latitude"]
            data["longitude"] = location["longitude"]
            data["country"] = location["country_name"]
            data["city"] = location["city"]
            data['region_code'] = location["region"]
            data["region"] = REGION_CODE_TO_REGION.get(data["region_code"])

        except:  # check https://pypi.org/project/geoip2/ for the exceptions thrown by GeoIP2
            data["latitude"] = None
            data["longitude"] = None
            data["country"] = "Unknown"
            data["city"] = "Unknown"
            data['region_code'] = "Unknown"
            data["region"] = "Unknown"

        # sometimes the Geolocation may not return some of the fields
        if not data["country"]:
            data["country"] = "Unknown"

        if not data["region_code"]:
            data["region_code"] = "Unknown"

        if not data["city"]:
            data["city"] = "Unknown"

        if not data["region"]:
            data["region"] = "Unknown"

        # enqueue job in the redis queue named 'middleware_log'
        REDIS_CLIENT.rpush('middleware_log', json.dumps(data))

    except Exception as e:
        with open("enqueue_middleware_log_errors.txt", "a") as f:
            f.write(str(e) + '\n')

    return HttpResponse(status=200)


# initialize the variable pointing to the tutorial_progress_logs
# MongoDB collection.
db = MONGO_CLIENT.logs
tutorial_progress_logs = db.tutorial_progress_logs


"""
API function called from the client-side Javascript for extracting Geolocation info,
and pushing the log to a redis queue.
"""
@csrf_exempt
@require_POST
def save_js_log (request):

    try:
        data = {}
        data["visit_duration"] = request.POST.get('visit_duration')
        data['referer'] = request.POST.get('referer')
        data['browser_family'] = request.POST.get('browser_family')
        data['browser_version'] = request.POST.get('browser_version')
        data['os_family'] = request.POST.get('os_family')
        data['os_version'] = request.POST.get('os_version')
        data['title'] = request.POST.get('title')
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
        data['device_type'] = request.POST.get ('device_type')

        if not data['referer']:
            data['referer'] = '(No referring link)'

        # enqueue job in the redis queue named 'js_log'
        REDIS_CLIENT.rpush('js_log', json.dumps(data))

    except Exception as e:
        with open("enqueue_js_log_errors.txt", "a") as f:
            f.write(str(e) + '\n')
    
    return HttpResponse(status=200)


"""
Function for handling the AJAX call of saving tutorial progress data. This AJAX
call is made in watch_tutorial.html. Calls update_tutorial_progress in utils.py
for the actual saving in MongoDB.
This code is currently not in use, as an API-based code is currently used instead.
TODO: don't let users make their own post requests to this view. Remove CSRF exempt
"""
@csrf_exempt
@require_POST
def save_tutorial_progress (request):

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
    data['allow_completion_change'] = request.POST.get("allow_completion_change")

    update_tutorial_progress (data)  # synchronous call

    return HttpResponse(status=200)


"""
Function for handling the AJAX call of changing tutorial completion data. This AJAX
call is made in watch_tutorial.html.
This code is currently not in use, as an API-based code is currently used instead.
TODO: don't let users make their own post requests to this view. Remove CSRF exempt
"""
@csrf_exempt
@require_POST
def change_completion (request):

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
        with open("change_completion_errors.txt", "a") as f:
            f.write(str(e) + '\n')
        
    return HttpResponse(status=500)


"""
Function for handling the AJAX call of checking tutorial completion. This AJAX
call is made in watch_tutorial.html.
This code is currently not in use, as an API-based code is currently used instead.
TODO: don't let users make their own post requests to this view. Remove CSRF exempt
"""
@csrf_exempt
@require_POST
def check_completion (request):

    # configurations for pymongo
    db = MONGO_CLIENT.logs
    tutorial_progress_logs = db.tutorial_progress_logs

    try:

        res = tutorial_progress_logs.find_one(
            { "username" : request.POST.get('username') }
        )

        if res['fosses'][str(request.POST.get('foss_id'))][str(request.POST.get('language_id'))][str(request.POST.get('tutorial_id'))]['completed'] == True:
            return HttpResponse(status=200)

    except Exception:  # the 'completed' field is not yet created for that log.
        pass
    
    return HttpResponse(status=500)