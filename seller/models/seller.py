from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models

class Seller(AbstractUser):
    groups = models.ManyToManyField(Group, related_name="seller_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="seller_permissions", blank=True)