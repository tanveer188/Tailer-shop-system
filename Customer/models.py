from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Customers(models.Model):
    organization = models.ForeignKey("Owner.Organization", on_delete=models.CASCADE)
    mobileno = models.IntegerField(unique=True,blank=True,null=True,validators=[
            MaxValueValidator(9999999999),
            MinValueValidator(1111111111)
        ])
    
    address = models.CharField(max_length=40)
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=50, blank=True)
    def __str__(self):
      return str(self.name)
class Measurement(models.Model):
  customers = models.OneToOneField(Customers,on_delete=models.PROTECT,blank=True,null=True)
  legs = models.DecimalField(max_digits=5, decimal_places=2)
  west = models.DecimalField(max_digits=5, decimal_places=2)
  hand = models.DecimalField(max_digits=5, decimal_places=2)
  def __str__(self):
      return str(self.customers.name)