from django.db import models


class Category(models.Model):
    image = models.ImageField(upload_to='images/category/')
    ru_name = models.CharField(max_length=255)
    uz_name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return f'{self.ru_name} | {self.uz_name}'