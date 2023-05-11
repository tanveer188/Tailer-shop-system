from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('worker',views.worker,name="worker"),
    path('allComplited',views.allComplited,name="allComplited"),
    path('customerinfo/<str:pk>',views.customerinfo,name="customerinfo"),
    path('billinfo/<str:pk>',views.billinfo,name="billinfo"),
    path('work/<str:fieldname>',views.work,name="work"),
    path('work/<str:fieldname>/<str:pk>',views.workstatus,name="workstatus"),
    path('completed',views.completed,name="completed"),
    path('search',views.search,name="search"),
]