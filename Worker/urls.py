from django.contrib import admin
from django.urls import path,include
from . import views
from django.urls import re_path as url

urlpatterns = [
    path('worker',views.worker,name="worker"),
    path('allComplited',views.allComplited,name="allComplited"),
    path('customerinfo/<str:pk>',views.customerinfo,name="customerinfo"),
    path('billinfo/<str:pk>',views.billinfo,name="billinfo"),
    path('work/<str:fieldname>',views.work,name="work"),
    path('work/<str:fieldname>/<str:pk>',views.workstatus,name="workstatus"),
    path('completed',views.completed,name="completed"),
    path('search',views.search,name="search"),
    path('organization',views.organization,name="organization"),
  url(
        r'^test-autocomplete/$',
        views.TestAutocomplete.as_view(),
        name='test-autocomplete',
    ),
]