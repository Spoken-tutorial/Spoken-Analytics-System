from django.urls import path
from django.conf.urls import url
from dashboard import views

urlpatterns = [
    # Serves dashboard
    path('', views.index, name="index"),
    # Serves data to graph at dashboard
    path('graph_data/', views.graphData, name="graph-data"),
    # Serves events page
    path('events', views.events, name="events"),
    # Serves data for data table at events page
    path('events_data/', views.eventsData, name="events-data"),
]