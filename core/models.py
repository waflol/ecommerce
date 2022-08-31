from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,null=False,blank=False,on_delete=models.CASCADE)
    
    #extra fields
    phone_field = models.CharField(max_length=12,blank=False)
    def __str__(self) -> str:
        return self.user.username
    
    