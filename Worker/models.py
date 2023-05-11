from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Worker_db(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    email = models.CharField(max_length=50, blank=True)
    def __str__(self):
      return str(self.user.username)
