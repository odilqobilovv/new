from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('vendor', 'Vendor'),
        ('admin', 'Admin'),
    )
    phone = models.IntegerField(unique=True, blank=True, null=True)
    payment_method = models.CharField(default=0, null=True, blank=True, max_length=16)
    first_registered_device = models.CharField(max_length=255, null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    image = models.ImageField(upload_to='images/user/', blank=True, null=True)