from django.db import models

from users.models.user import User

class Shop(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=455)
    image = models.ImageField(upload_to='images/shop/')

    def __str__(self):
        return f'{self.owner} | {self.name}'