from __future__ import unicode_literals
from djongo import models

# Create your models here.
class Log(models.Model):
    path_info = models.CharField (max_length=200)
    browser_info = models.CharField (max_length=300)
    method = models.CharField(max_length=10)
    event_name = models.CharField (max_length=100, blank=False)
    visited_by = models.CharField (max_length=100, blank=False)
    ip_address = models.GenericIPAddressField(null=False)
    country = models.CharField (max_length=100, blank=False)
    state_code = models.CharField (max_length=5, blank=False)
    city = models.CharField (max_length=100, blank=False)
    datetime = models.DateTimeField()
    
    def __str__(self):
        return "Website Log Object"

    objects = models.DjongoManager()

class DailyStats(models.Model):
    date = models.DateTimeField()
    page_views = models.IntegerField()
    unique_visits = models.IntegerField()
    first_time_visits = models.IntegerField()
    returning_visits = models.IntegerField()
    unique_visitors = models.IntegerField()

    def __str__(sekf):
        return "Daily Stats"

    objects = models.DjongoManager()

class WeeklyStats(models.Model):
    week_of_year = models.IntegerField()
    year = models.IntegerField()
    page_views = models.IntegerField()
    unique_visits = models.IntegerField()
    first_time_visits = models.IntegerField()
    returning_visits = models.IntegerField()
    unique_visitors = models.IntegerField()

    def __str__(sekf):
        return "Weekly Stats"

    objects = models.DjongoManager()

class MonthlyStats(models.Model):
    month_of_year = models.IntegerField()
    year = models.IntegerField()
    page_views = models.IntegerField()
    unique_visits = models.IntegerField()
    first_time_visits = models.IntegerField()
    returning_visits = models.IntegerField()
    unique_visitors = models.IntegerField()

    def __str__(sekf):
        return "Monthly Stats"

    objects = models.DjongoManager()