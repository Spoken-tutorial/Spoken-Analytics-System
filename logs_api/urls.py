from django.conf.urls import url
from logs_api.views import *

app_name = 'logs_api'

urlpatterns = [
    url(r'^save_website_log/$', save_website_log, name='save_website_log'),
]