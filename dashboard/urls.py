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
    re_path('^event_analysis/(?P<event_name>[\w.]+)/$', views.eventAnalysis, name="event-analysis"),
    # Serves data to event analysis page
    re_path('^event_graph_data/$', views.eventAnalysisGraphData, name="event-analysis-graph-data"),
    # Serves report page
    re_path('^reports/$', views.reports, name="reports"),
    # Serves reports stats
    re_path('^reports_stats/$', views.getReportsStats, name="reports-stats"),
    # Serves foss page
    re_path('^foss/$', views.foss, name="foss"),
    # Serves data for data table at foss page
    re_path('^foss_data/$', views.fossData, name="foss-data"),
    # Serves location report page
    re_path('^location_report/$', views.locationReport, name="location-report"),
]