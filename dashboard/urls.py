from django.urls import path
from django.conf.urls import url
from dashboard import views

urlpatterns = [
    path('', views.index),
    # to serve daily data to graph at dashboard
    path('daily_graph_data/', views.dailyGraphData, name="daily-graph-data"),
    # to serve weekly data to graph at dashboard
    path('daily_graph_data/', views.weeklyGraphData, name="weekly-graph-data"),
]