from django.db import models

from user.models import User


# Create your models here.models

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    img = models.ImageField(upload_to='products/', verbose_name='изображение', null=True)
    attendees = models.ManyToManyField(User, related_name='events')

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    img = models.ImageField(upload_to='articles/', null=True)

    def __str__(self):
        return self.title
