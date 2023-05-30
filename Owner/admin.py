from django.contrib import admin
from .models import Work,Organization,Member,Types
# Register your models here.
admin.site.register([Work,Organization,Member,Types])