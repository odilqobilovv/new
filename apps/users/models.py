from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    phone = models.IntegerField(unique=True, blank=True, null=True)
    payment_method = models.IntegerField(default=0, null=True, blank=True)
    first_registered_device = models.CharField(max_length=255, null=True, blank=True)