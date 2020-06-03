"""
This script calculates the daily, weekly, monthly and yearly average stats.
It takes stats from 'DailyStats', 'WeeklyStats', 'MonthlyStats' and 'YearlyStats'
then calculates average and stores them to 'AverageStats'.

The script runs everyday after 12:05 AM.
"""
import datetime
from dashboard.models import Log, DailyStats, WeeklyStats, MonthlyStats, YearlyStats, AverageStats
from pytz import timezone
from django.conf import settings
from celery import shared_task

@shared_task(bind=True)
def average_statistics(self):

    tz = timezone(settings.TIME_ZONE)
        
    # Fetching data from collections
    daily_stats = DailyStats.objects.all() 
    weekly_stats = WeeklyStats.objects.all()
    monthly_stats = MonthlyStats.objects.all()
    yearly_stats = YearlyStats.objects.all()
    all_logs_total = Log.objects.all().count()

    # Variables to store stats
    total_records = 0
    total_page_views = 0
    total_unique_visits = 0
    total_first_time_visits = 0
    total_returning_visits = 0

    # Calculating average daily stats
    for stats in daily_stats:
        total_records += 1
        total_page_views += stats.page_views
        total_unique_visits += stats.unique_visits
        total_first_time_visits += stats.first_time_visits
        total_returning_visits += stats.returning_visits


    average_daily_page_views = int(total_page_views/total_records)
    average_daily_unique_visits = int(total_unique_visits/total_records)
    average_daily_first_time_visits = int(total_first_time_visits/total_records)
    average_daily_returning_visits = int(total_returning_visits/total_records)

    # Variables to store stats
    total_records = 0
    total_page_views = 0
    total_unique_visits = 0
    total_first_time_visits = 0
    total_returning_visits = 0

    # Calculating average weekly stats
    for stats in weekly_stats:
        total_records += 1
        total_page_views += stats.page_views
        total_unique_visits += stats.unique_visits
        total_first_time_visits += stats.first_time_visits
        total_returning_visits += stats.returning_visits


    average_weekly_page_views = int(total_page_views/total_records)
    average_weekly_unique_visits = int(total_unique_visits/total_records)
    average_weekly_first_time_visits = int(total_first_time_visits/total_records)
    average_weekly_returning_visits = int(total_returning_visits/total_records)

    # Variables to store stats
    total_records = 0
    total_page_views = 0
    total_unique_visits = 0
    total_first_time_visits = 0
    total_returning_visits = 0

    # Calculating average monthly stats
    for stats in monthly_stats:
        total_records += 1
        total_page_views += stats.page_views
        total_unique_visits += stats.unique_visits
        total_first_time_visits += stats.first_time_visits
        total_returning_visits += stats.returning_visits


    average_monthly_page_views = int(total_page_views/total_records)
    average_monthly_unique_visits = int(total_unique_visits/total_records)
    average_monthly_first_time_visits = int(total_first_time_visits/total_records)
    average_monthly_returning_visits = int(total_returning_visits/total_records)

    # Variables to store stats
    total_records = 0
    total_page_views = 0
    total_unique_visits = 0
    total_first_time_visits = 0
    total_returning_visits = 0

    # Calculating average yearly stats
    for stats in yearly_stats:
        total_records += 1
        total_page_views += stats.page_views
        total_unique_visits += stats.unique_visits
        total_first_time_visits += stats.first_time_visits
        total_returning_visits += stats.returning_visits


    average_yearly_page_views = int(total_page_views/total_records)
    average_yearly_unique_visits = int(total_unique_visits/total_records)
    average_yearly_first_time_visits = int(total_first_time_visits/total_records)
    average_yearly_returning_visits = int(total_returning_visits/total_records)

    # making AverageStats object
    avg_stats = AverageStats()

    avg_stats.average_daily_page_views = average_daily_page_views
    avg_stats.average_daily_unique_visits = average_daily_unique_visits
    avg_stats.average_daily_first_time_visits = average_daily_first_time_visits
    avg_stats.average_daily_returning_visits = average_daily_returning_visits

    avg_stats.average_weekly_page_views = average_weekly_page_views
    avg_stats.average_weekly_unique_visits = average_weekly_unique_visits
    avg_stats.average_weekly_first_time_visits = average_weekly_first_time_visits
    avg_stats.average_weekly_returning_visits = average_weekly_returning_visits

    avg_stats.average_monthly_page_views = average_monthly_page_views
    avg_stats.average_monthly_unique_visits = average_monthly_unique_visits
    avg_stats.average_monthly_first_time_visits = average_monthly_first_time_visits
    avg_stats.average_monthly_returning_visits = average_monthly_returning_visits

    avg_stats.average_yearly_page_views = average_yearly_page_views
    avg_stats.average_yearly_unique_visits = average_yearly_unique_visits
    avg_stats.average_yearly_first_time_visits = average_yearly_first_time_visits
    avg_stats.average_yearly_returning_visits = average_yearly_returning_visits

    avg_stats.total_page_views = all_logs_total
    avg_stats.datetime = tz.localize(datetime.datetime.now() - datetime.timedelta(1))

    # Saving the object
    avg_stats.save()