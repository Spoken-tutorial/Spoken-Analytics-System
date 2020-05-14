from django.shortcuts import render
import redis
import datetime
import json 
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

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
        data['browser_info'] = request.POST.get('browser_info')  # request.META['HTTP_USER_AGENT']
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
        # enqueue job in the redis queue named 'tasks3'
        redis_client.rpush('tasks3', json.dumps(data))

    except Exception as e:
        print("Log Exception " + str(e))
    
    return HttpResponse(status=200)