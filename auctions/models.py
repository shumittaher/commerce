from django.contrib.auth.models import AbstractUser
from django.db import models

class Listings(models.Model):
    object_id = models.AutoField(primary_key=True)
    object_name = models.CharField(max_length=64)
    object_price = models.DecimalField(decimal_places=2, max_digits=8)
    object_description = models.TextField(blank=True)
    picture_URL = models.URLField()
    object_lister = models.ForeignKey("User", on_delete=models.CASCADE)
    listing_open = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.object_name}"
    
class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    object_id = models.ForeignKey(Listings, on_delete=models.CASCADE)
    comment_text = models.TextField()

class User(AbstractUser):
    phone_number = models.CharField(max_length = 11)
    watchlisted = models.ManyToManyField(Listings)

class Bids(models.Model):
    bid_id = models.AutoField(primary_key=True)
    object_id = models.ForeignKey(Listings, on_delete=models.CASCADE)
    bid_amount= models.DecimalField(decimal_places=2, max_digits=8)
    bidder_id = models.ForeignKey(User, on_delete=models.CASCADE)
