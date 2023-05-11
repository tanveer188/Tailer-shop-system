from django.contrib import admin
from .models import Customers,Measurement
# Register your models here.
admin.site.register([Customers,Measurement])