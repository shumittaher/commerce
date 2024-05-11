from django.contrib import admin
from .models import Listings, Categories, User, Comments, Bids

# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ('object_name', 'object_price', 'category', 'object_lister')
class BidsAdmin(admin.ModelAdmin):
    list_display = ( 'object_id', 'bid_amount', 'bidder_id')
class CommentsAdmin(admin.ModelAdmin):
    list_display = ( 'object_id', 'comment_text', 'commenter_id')


admin.site.register(User)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Listings, ListingAdmin)
admin.site.register(Categories)
admin.site.register(Bids, BidsAdmin)


