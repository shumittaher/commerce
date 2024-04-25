from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length = 11)
    pass


class Listings(models.Model):
    object_id = models.AutoField(primary_key=True)
    object_name = models.CharField(max_length=64)
    object_price = models.DecimalField(decimal_places=2, max_digits=8)
    object_description = models.TextField(blank=True)
    picture_URL = models.URLField()
