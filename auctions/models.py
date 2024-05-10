from django.contrib.auth.models import AbstractUser
from django.db import models

class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_text = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return f"{self.category_text}"

class Listings(models.Model):
    object_id = models.AutoField(primary_key=True)
    object_name = models.CharField(max_length=64)
    object_price = models.DecimalField(decimal_places=2, max_digits=8)
    object_description = models.TextField(blank=True)
    picture_URL = models.URLField()
    object_lister = models.ForeignKey("User", on_delete=models.CASCADE)
    listing_open = models.BooleanField(default=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.object_name}"

class User(AbstractUser):
    phone_number = models.CharField(max_length = 11)
    watchlisted = models.ManyToManyField(Listings)

class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    object_id = models.ForeignKey(Listings, on_delete=models.CASCADE)
    comment_text = models.TextField(max_length=255)
    commenter_id = models.ForeignKey(User, on_delete=models.CASCADE)

class Bids(models.Model):
    bid_id = models.AutoField(primary_key=True)
    object_id = models.ForeignKey(Listings, on_delete=models.CASCADE)
    bid_amount= models.DecimalField(decimal_places=2, max_digits=8)
    bidder_id = models.ForeignKey(User, on_delete=models.CASCADE)
