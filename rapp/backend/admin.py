from django.contrib import admin
from .models import Patient, Region,Disease,Sign

admin.site.register(Patient)
admin.site.register(Region)
admin.site.register(Disease)
admin.site.register(Sign)
# Register your models here.
