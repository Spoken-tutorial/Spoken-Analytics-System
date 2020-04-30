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
    datetime = models.DateTimeField(auto_now_add=True, auto_now=False)
    
    def __str__(self):
        return "Website Log Object"
    objects = models.DjongoManager()
    # URLField
    # help_text="Please use the following format: <em>YYYY-MM-DD</em>."