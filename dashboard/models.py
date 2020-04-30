from django.db import models

# Create your models here.
class Log(models.Model):
    # Model used to store and retrieve logs from database
    
    path_info = models.CharField(max_length=1023)
    browser_info = models.CharField(max_length=255)
    request_data = models.CharField(max_length=2047)
    method = models.CharField(max_length=7)
    event_name = models.CharField(max_length=1023)
    visited_by = models.CharField(max_length=255)
    city = models.CharField(max_length=50, null=True)
    region = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    ip_address = models.CharField(max_length=50)
    view_args = models.CharField(max_length=1023, null=True)
    view_kwargs = models.CharField(max_length=1023, null=True)
    timestamp = models.DateTimeField()
    
    def __str__(self):
        return self.path_info