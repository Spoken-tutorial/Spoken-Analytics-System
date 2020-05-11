from django.urls import path, re_path
from django.conf.urls import url
from dashboard import views

urlpatterns = [
    # Serves dashboard
    re_path('^$', views.index, name="index"),
    # Serves data to graph at dashboard
    re_path('^graph_data/$', views.graphData, name="graph-data"),
    # Serves events page
    re_path('^events/$', views.events, name="events"),
    # Serves data for data table at events page
    re_path('^events_data/$', views.eventsData, name="events-data"),
    # Serves event analysis page
    re_path('^event_analysis/(?P<event_name>[\w.]+)/$', views.eventAnalysis, name="event-analysis")
]