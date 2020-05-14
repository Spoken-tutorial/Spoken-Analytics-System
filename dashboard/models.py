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
    region = models.CharField (max_length=5, blank=False)
    city = models.CharField (max_length=100, blank=False)
    datetime = models.DateTimeField()
    
    def __str__(self):
        return "Website Log Object"

    objects = models.DjongoManager()


class AverageStats(models.Model):
    average_daily_page_views = models.IntegerField()
    average_daily_unique_visits = models.IntegerField()
    average_daily_first_time_visits = models.IntegerField()
    average_daily_returning_visits = models.IntegerField()
    average_weekly_page_views = models.IntegerField()
    average_weekly_unique_visits = models.IntegerField()
    average_weekly_first_time_visits = models.IntegerField()
    average_weekly_returning_visits = models.IntegerField()
    average_monthly_page_views = models.IntegerField()
    average_monthly_unique_visits = models.IntegerField()
    average_monthly_first_time_visits = models.IntegerField()
    average_monthly_returning_visits = models.IntegerField()
    average_yearly_page_views = models.IntegerField()
    average_yearly_unique_visits = models.IntegerField()
    average_yearly_first_time_visits = models.IntegerField()
    average_yearly_returning_visits = models.IntegerField()
    total_page_views = models.IntegerField()
    
    def __str__(self):
        return "Average Stats Object"

    objects = models.DjongoManager()


class DailyStats(models.Model):
    date = models.DateTimeField()
    page_views = models.IntegerField()
    unique_visits = models.IntegerField()
    first_time_visits = models.IntegerField()
    returning_visits = models.IntegerField()
    unique_visitors = models.IntegerField()

    def __str__(self):
        return "Daily Stats"

    objects = models.DjongoManager()


class WeeklyStats(models.Model):
    date = models.DateTimeField()
    week_of_year = models.IntegerField()
    year = models.IntegerField()
    page_views = models.IntegerField()
    unique_visits = models.IntegerField()
    first_time_visits = models.IntegerField()
    returning_visits = models.IntegerField()
    unique_visitors = models.IntegerField()

    def __str__(self):
        return "Weekly Stats"

    objects = models.DjongoManager()


class MonthlyStats(models.Model):
    date = models.DateTimeField()
    month_of_year = models.IntegerField()
    year = models.IntegerField()
    page_views = models.IntegerField()
    unique_visits = models.IntegerField()
    first_time_visits = models.IntegerField()
    returning_visits = models.IntegerField()
    unique_visitors = models.IntegerField()

    def __str__(self):
        return "Monthly Stats"

    objects = models.DjongoManager()


class YearlyStats(models.Model):
    date = models.DateTimeField()
    year = models.IntegerField()
    page_views = models.IntegerField()
    unique_visits = models.IntegerField()
    first_time_visits = models.IntegerField()
    returning_visits = models.IntegerField()
    unique_visitors = models.IntegerField()

    def __str__(self):
        return "Yearly Stats"

    objects = models.DjongoManager()

class EventStats(models.Model):
    event_name = models.CharField(max_length=100, blank=False)
    path_info = models.CharField (max_length=200)
    date = models.DateTimeField()
    unique_visits = models.IntegerField()

    def __str__(self):
        return "Event Stats"

    objects = models.DjongoManager()

class FossStats(models.Model):
    foss_name = models.CharField(max_length=100)
    date = models.DateTimeField()
    page_views = models.IntegerField()
    unique_visits = models.IntegerField()

    def __str__(self):
        return "Foss Stats"

    objects = models.DjongoManager()

class RegionStats(models.Model):
    region = models.CharField(max_length=100)
    page_views = models.IntegerField()

    def __str__(self):
        return "Region Stats"

    objects = models.DjongoManager()

class CityStats(models.Model):
    city = models.CharField(max_length=100)
    page_views = models.IntegerField()

    def __str__(self):
        return "City Stats"

    objects = models.DjongoManager()