from django.db import models
from django.contrib.auth.models import User
from Customer.models import Customers
from django.conf import settings
from django.utils.html import format_html

# Create your models here.
from dal import autocomplete
class Organization(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
      return str(self.name)
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    is_owner = models.BooleanField(default=False)
    def __str__(self):
      return str(self.organization.name +":"+ self.user.username)
class Types(models.Model):
  name= models.CharField(max_length=60)
  organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
  def __str__(self):
    return str(self.name)
class Work(models.Model):
  class MaterialChoices(models.TextChoices):
    STAGE1 = 'No Need', 'No Need'
    STAGE2 = 'Need', 'Need'
    STAGE3 = 'Fulfilled', 'Fulfilled'
    STAGE4 = 'Provided', 'Provided'
  class TaskChoices(models.TextChoices):
    STAGE1 = 'No Need', 'No Need'
    STAGE2 = 'Need', 'Need'
    STAGE3 = 'Fulfilled', 'Fulfilled'
  organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
  worker = models.ForeignKey(Member, on_delete=models.CASCADE)
  billno = models.CharField(max_length=10,unique=True)
  type = models.ForeignKey(Types,on_delete=models.PROTECT,)
  customer = models.ForeignKey(Customers,on_delete=models.CASCADE)
  date = models.DateField()
  astar = models.CharField(max_length=30,choices=MaterialChoices.choices,default=MaterialChoices.STAGE1)
  piku = models.CharField(max_length=30,choices=TaskChoices.choices,default=TaskChoices.STAGE1)
  completed = models.BooleanField(default=False)
  delivered = models.BooleanField(default=False)
  cost = models.IntegerField()
  bill_pdf = models.FileField(null=True, blank=True)
  def __str__(self):
      return str(self.customer.name)+" billno:"+str(self.billno)
  def save(self, *args, **kwargs):
        if self.organization != self.worker.organization:
            raise ValueError("The organization and worker must belong to the same organization.")
        super().save(*args, **kwargs)
  def get_relative_file_path(self):
        return "media"+str(self.bill_pdf).replace(str(settings.MEDIA_ROOT), '')

  def get_file_link(self):
      if self.bill_pdf:
        file_path = self.get_relative_file_path()
        return format_html('<a href="{}">{}</a>', file_path, file_path)
      return ''

# class Admin_class(models.Model):
#     profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
#     # work = models.models.ManyToManyField("",blank=True)
    
    
