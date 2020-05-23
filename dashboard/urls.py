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
    # Serves came from activity page
    re_path('^came_from_activity/$', views.cameFromActivity, name="came-from-activity"),
    # Serves download activity page
    re_path('^download_activity/$', views.downloadActivity, name="download-activity"),
    # Serves exit link activity page
    re_path('^exit_link_activity/$', views.exitLinkActivity, name="exit-link-activity"),
    # Serves visitor map page
    re_path('^visitor_map/$', views.visitorMap, name="visitor-map"),
    # Serves page view activity page
    re_path('^page_view_activity/$', views.pageViewActivity, name="page-view-activity"),
    # Serves visitor activity page
    re_path('^visitor_activity/$', views.visitorActivity, name="visitor-activity"),
    # Serves visitor paths page
    re_path('^visitor_path/$', views.visitorPath, name="visitor-path"),
    # Serves keyword activity page
    re_path('^kayword_activity/$', views.keywordActivity, name="keyword-activity"),
    # Serves magnify page
    re_path('^magnify/$', views.magnify, name="magnify"),
    # Serves foss-page report page
    re_path('^foss_event_report/$', views.fossEventReport, name="foss-event-report"),
    # Serves system report page
    re_path('^system_report/$', views.systemReport, name="system-report"),
    # Serves traffic report page
    re_path('^traffic_report/$', views.trafficReport, name="traffic-report"),
]