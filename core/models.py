from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
   phone_number = models.CharField(max_length=15, null = True, blank= True, unique=True)
    
   # USERNAME_FIELD = "phone_number"    
    
   def __str__(self):
        return self.username