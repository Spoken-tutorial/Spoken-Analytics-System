from __future__ import unicode_literals
from djongo import models
from djgeojson.fields import PointField

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
    page_views = models.IntegerField()
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

class CameFromActivity(models.Model):
    datetime = models.DateTimeField()
    referrer = models.CharField(max_length=300)
    entry_page = models.CharField(max_length=300)

    def __str__(self):
        return "Came From Activity Model"

    objects = models.DjongoManager()

class DownloadActivity(models.Model):
    datetime = models.DateTimeField()
    download_link = models.CharField(max_length=300)
    clicked_from = models.CharField(max_length=300)

    def __str__(self):
        return "Download Activity Model"

    objects = models.DjongoManager()

class ExitLinkActivity(models.Model):
    datetime = models.DateTimeField()
    exit_link_clicked = models.CharField(max_length=300)
    exit_page = models.CharField(max_length=300)

    def __str__(self):
        return "Exit Link Activity Model"

    objects = models.DjongoManager()

class VisitorSpot(models.Model):
    datetime = models.DateTimeField()
    geom = PointField()
    ip_address = models.GenericIPAddressField()

    @property
    def popupContent(self):
      return '<span/>{}</span>'.format(self.ip_address)
    
class PageViewActivity(models.Model):
    datetime = models.DateTimeField()
    browser = models.CharField(max_length=100)
    os = models.CharField(max_length=100)
    screen_res = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    language = models.CharField(max_length=25)
    ip_address = models.GenericIPAddressField()
    isp = models.CharField(max_length=100)
    page_name = models.CharField(max_length=300)
    page_url = models.CharField(max_length=300)
    referrer = models.CharField(max_length=300)

    def __str__(self):
        return "Page View Activity Model"

    objects = models.DjongoManager()

class VisitorActivity(models.Model):
    page_views = models.IntegerField()
    total_visits = models.IntegerField()
    latest_page_view = models.DateTimeField()
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    visit_length_sec = models.IntegerField()
    ip_address = models.GenericIPAddressField()
    isp = models.CharField(max_length=100)
    screen_res = models.CharField(max_length=20)
    browser = models.CharField(max_length=100)
    os = models.CharField(max_length=100)
    referrer = models.CharField(max_length=300)
    entry_page = models.CharField(max_length=300)
    latest_page = models.CharField(max_length=300)
    visit_page = models.CharField(max_length=300)

    def __str__(self):
        return "Visitor Activity Model"

    objects = models.DjongoManager()

class Path(models.Model):
    datetime = models.DateTimeField()
    referrer = models.CharField(max_length=300)
    page_url = models.CharField(max_length=300)
    
    class Meta:
        abstract = True

class VisitorPath(models.Model):
    datetime = models.DateTimeField()
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    isp = models.CharField(max_length=100)
    visit_num = models.IntegerField()
    screen_res = models.CharField(max_length=20)
    browser = models.CharField(max_length=100)
    os = models.CharField(max_length=100)
    path = models.ArrayField(
        model_container=Path,
    )

    def __str__(self):
        return "Visitor Path Model"

    objects = models.DjongoManager()


class KeywordActivity(models.Model):
    datetime = models.DateTimeField()
    name = models.CharField(max_length=100)
    search_query = models.CharField(max_length=300)
    entry_page = models.CharField(max_length=300)

    def __str__(self):
        return "Keyword Activity Model"

    objects = models.DjongoManager()