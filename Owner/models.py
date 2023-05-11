from django.db import models
from django.contrib.auth.models import User
from Customer.models import Customers
from Worker.models import Worker_db
# Create your models here.
class Owner_db(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    email = models.CharField(max_length=50, blank=True)
    def __str__(self):
      return str(self.user.username)
    # role = models.ManyToManyField("app.Model",)
    # individual_work = models.ManyToManyField("app.Model")
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
  
  worker = models.ManyToManyField(Worker_db,blank=True)
  workDone = models.ManyToManyField(Worker_db,blank=True,related_name="workDone")
  billno = models.CharField(max_length=10, blank=True,unique=True)
  customer = models.ForeignKey(Customers,on_delete=models.CASCADE)
  date = models.DateField()
  astar = models.CharField(max_length=30,choices=MaterialChoices.choices,default=MaterialChoices.STAGE1)
  piku = models.CharField(max_length=30,choices=TaskChoices.choices,default=TaskChoices.STAGE1)
  completed = models.BooleanField(default=False)
  delivered = models.BooleanField(default=False)
  cost = models.IntegerField()
  def __str__(self):
      return str(self.customer.name)+" billno:"+str(self.billno)
# class Admin_class(models.Model):
#     profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
#     # work = models.models.ManyToManyField("",blank=True)
    
    
