from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models

# Create your models here.

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('vendor', 'Vendor'),
        ('admin', 'Admin'),
    )
    phone = models.CharField(unique=True, blank=True, null=True, max_length=15)
    payment_method = models.CharField(default=0, null=True, blank=True, max_length=16)
    # first_registered_device = models.CharField(max_length=255, null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')
    image = models.ImageField(upload_to='images/user/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, related_name="user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="user_permissions", blank=True)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)