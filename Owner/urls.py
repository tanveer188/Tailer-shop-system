from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('homepage',views.homepage,name="homepage"),
    path('newbill',views.newbill,name="newbill"),
    path('newcustomer',views.newcustomer,name="newcustomer"),
    path('newmeasurment/<str:pk>',views.newmeasurment,name="newmeasurment"),
    path('delivered',views.delivered,name="delivered"),
    path('Edit/<str:model_name>/<str:pk>',views.Edit,name="Edit"),
    path('newmember',views.newmember,name="newmember"),
    path('delete/<str:model_name>',views.delete,name="delete"),
    path('bill/<str:pk>',views.bill_maker,name="bill_maker"),
    path('typepage',views.typepage,name="typepage"),
    path('newtype',views.newtype,name="newtype"),
]
