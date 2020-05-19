from django.contrib import admin
from .models import Log, VisitorSpot
from leaflet.admin import LeafletGeoAdmin

# Register your models here.
admin.site.register(Log)
admin.site.register(VisitorSpot, LeafletGeoAdmin)
