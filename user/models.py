from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

# from catalog.models import NULLABLE
NULLABLE = {'blank': True, 'null': True}


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='почта', unique=True, max_length=255)
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    first_name = models.CharField(max_length=255, null=True, verbose_name='имя')
    last_name = models.CharField(max_length=255, null=True, verbose_name='фамилия')
    tg_link = models.CharField(max_length=255, null=True, verbose_name='ник в телеграм')
    course = models.CharField(max_length=255, null=True, verbose_name='курс')
    direction = models.TextField(null=True, verbose_name='направление')
    age = models.IntegerField(null=True, verbose_name='возраст')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
