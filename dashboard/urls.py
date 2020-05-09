from django.urls import path
from django.conf.urls import url
from dashboard import views

urlpatterns = [
    path('', views.index, name="index"),
    # To serve daily data to graph at dashboard
    path('graph_data/', views.graphData, name="graph-data"),
    path('events', views.events, name="events")
]