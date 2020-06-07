import redis
import datetime
import json 
import math
import re
import time
import reverse_geocoder as rg 
import pycountry

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

    try:

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

        if 'post_data' in data:
            data['post_data'] = json.loads (data['post_data'])
        
        
        # if the address is not a properly formatted IPv4 or IPv6, reject the log
        if not re.match(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', data["ip_address"]):
            if not re.match(r'^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$', data['ip_address']):
                return


        # extract Geolocation info
        data['region'] = None

        try:
        
            location = GEOIP2_CLIENT.city(data['ip_address'])
            data["latitude"] = location["latitude"]
            data["longitude"] = location["longitude"]
            data["country"] = location["country_name"]
            data["city"] = location["city"]
            data["region"] = location["region"]

            if data['country'].upper() == "INDIA":
                data["region"] = REGION_CODE_TO_REGION.get(data["region"])

        except:  # check https://pypi.org/project/geoip2/ for the exceptions thrown by GeoIP2
            data["latitude"] = None
            data["longitude"] = None
            data["country"] = "Unknown"
            data["city"] = "Unknown"
            data["region"] = "Unknown"

        # sometimes the Geolocation may not return some of the fields
        if not data["country"]:
            data["country"] = "Unknown"

        if not data["region"]:
            data["region"] = "Unknown"

        if not data["city"]:
            data["city"] = "Unknown"

        print (data)
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

        data['datetime'] = str(datetime.datetime.fromtimestamp(int (data["datetime"])/1000))
        data['latitude'] = float (data['latitude'])
        data['longitude'] = float (data['longitude'])
        data['view_args'] = []
        data['view_kwargs'] = {}

        """
        If the user lets the browser have location access, we get their accurate
        coordinates, which we can convert to a location using the reverse_geocoder library.
        However, the reverse_geocoder library is slow, and hence the following code is commented out.
        Currently using placeholders.
        """
        if data['country'] == "" or data['region'] == "" or data['city'] == "":

        #     # perform reverse geocoding
        #     try:

        #         rg_result = rg.search((data["latitude"], data["longitude"])) 
        #         data['region'] = rg_result[0]['admin1']
        #         data['city'] = rg_result[0]['name']
        #         country_code = rg_result[0]['cc']
        #         data['country'] = pycountry.countries.get(alpha_2=country_code).name

        #     except:

        #         # in case the reverse geocoding did not return a field.
        #         if not data["country"]:
        #             data["country"] = "Unknown"

        #         if not data["region"]:
        #             data["region"] = "Unknown"

        #         if not data["city"]:
        #             data["city"] = "Unknown"

            data['country'] = 'India'
            data['region'] = 'Maharashtra'
            data['city'] = 'Mumbai'

        # enqueue job in the redis queue named 'js_log'
        REDIS_CLIENT.rpush('js_log', json.dumps(data))

    except Exception as e:
        with open("enqueue_js_log_errors.txt", "a") as f:
            f.write(str(e) + '\n')

    return HttpResponse(status=200)


exit_link_logs = db.exit_link_logs

"""
API function called from the client-side Javascript for saving exit link info.
"""
@csrf_exempt
@require_POST
def save_exit_info (request):

    try:
        data = {}
        data['datetime'] = datetime.datetime.fromtimestamp(int (request.POST.get("datetime"))/1000)
        data['exit_link_clicked'] = request.POST.get('exit_link_clicked')
        data['exit_link_page'] = request.POST.get('exit_link_page')

        # enqueue job in the redis queue named 'js_log'
        # REDIS_CLIENT.rpush('js_log', json.dumps(data))
        exit_link_logs.insert_one (data)

    except Exception as e:
        with open("exit_link_logs_errors.txt", "a") as f:
            f.write(str(e) + '\n')
    
    return HttpResponse(status=200)


"""
Function for handling the AJAX call of saving tutorial progress data. This AJAX
call is made in watch_tutorial.html. Calls update_tutorial_progress in utils.py
for the actual saving in MongoDB.
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