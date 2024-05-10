from django.contrib import admin
from .models import Listings, Categories, User, Comments, Bids

# Register your models here.

admin.site.register(Listings)
admin.site.register(Categories)
