from django.db import models

from seller.models import Seller


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="team")
    members = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="member_team")

    def __str__(self):
        return self.name