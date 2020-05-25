import redis
import datetime
import json 
import math
import re

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
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


@csrf_exempt
def middleware_log (request):
    
    data = {}
    data['ip_address'] = request.POST.get('ip_address')
    data['path_info'] = request.POST.get('path_info')
    data['browser_info'] = request.POST.get('browser_info')
    data['event_name'] = request.POST.get('event_name')
    data['visited_by'] = request.POST.get('visited_by')
    data['ip_address'] = request.POST.get('ip_address')
    data['method'] = request.POST.get('method')
    data['datetime'] = request.POST.get('datetime')
    data['referer'] = request.POST.get('referer')
    data['browser_family'] = request.POST.get('browser_family')
    data['browser_version'] = request.POST.get('browser_version')
    data['os_family'] = request.POST.get('os_family')
    data['os_version'] = request.POST.get('os_version')
    data['device_family'] = request.POST.get('device_family')
    data['device_type'] = request.POST.get('device_type')
    data['first_time_visit'] = request.POST.get ('first_time_visit')

    try:

        # if the IPv4 or IPv6 address is not a properly formatted IPv4, reject it
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

        # enqueue job in the redis queue named 'tasks4'
        REDIS_CLIENT.rpush('tasks4', json.dumps(data))

    except Exception as e:
        with open("enqueue_logs_errors.txt", "a") as f:
            f.write(str(e))


# initialize the variable pointing to the tutorial_progress_logs
# MongoDB collection.
db = MONGO_CLIENT.logs
tutorial_progress_logs = db.tutorial_progress_logs


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
        REDIS_CLIENT.rpush('tasks3', json.dumps(data))

    except Exception as e:
        print("Log Exception " + str(e))
    
    return HttpResponse(status=200)


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