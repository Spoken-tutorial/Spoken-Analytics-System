from django.conf.urls import url
from logs_api.views import *

app_name = 'logs_api'

urlpatterns = [
    url('save_middleware_log/', save_middleware_log, name='save_middleware_log'),
    url('save_js_log/', save_js_log, name='save_js_log'),
    url('save_tutorial_progress/', save_tutorial_progress, name='save_tutorial_progress'),
    url('change_completion/', change_completion, name='change_completion'),
    url('check_completion/', check_completion, name='check_completion'),
]