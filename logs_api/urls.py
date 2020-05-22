from django.conf.urls import url
from logs_api.views import *

app_name = 'logs_api'

urlpatterns = [
    url('save_website_log/', save_website_log, name='save_website_log'),
    url('save_tutorial_progress/', save_tutorial_progress, name='save_tutorial_progress'),
    url('change_completion/', change_completion, name='change_completion'),
    url('check_completion/', check_completion, name='check_completion'),
]