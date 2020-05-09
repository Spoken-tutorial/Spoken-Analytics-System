from django.contrib import admin
from .models import Log, DailyStats, WeeklyStats, MonthlyStats, YearlyStats, AverageStats

# Register your models here.
admin.site.register(Log)
admin.site.register(DailyStats)
admin.site.register(WeeklyStats)
admin.site.register(MonthlyStats)
admin.site.register(YearlyStats)
admin.site.register(AverageStats)