from django.forms import ModelForm
from .models import Work

from Customer.models import Measurement,Customers

class WorkFoam(ModelForm):
  class Meta:
    model = Work
    fields = ("billno","customer","date","astar","piku","cost","worker")
class CustomerFoam(ModelForm):
  class Meta:
    model = Customers
    fields = ("mobileno","name","address","email")
class MeasurementFoam(ModelForm):
  class Meta:
    model = Measurement
    fields = ("legs","west","hand")