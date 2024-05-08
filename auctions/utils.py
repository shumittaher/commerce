from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import Item_user_combo
from .models import Listings, Bids


def check_post_method(view_func):
    def wrapper(request, *args, **kwargs):
        
        if request.method == 'POST':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("index"))
        
    return wrapper

def login_required(view_func):
    
    def wrapper(request, *args, **kwargs):

        if not (request.user.is_authenticated):
            return HttpResponseRedirect(reverse("login"))
        
        else: 
            return view_func(request, *args, **kwargs)

    return wrapper

def process_user_item_combo(request):

    user_item = Item_user_combo(request.POST)

    if user_item.is_valid():
        object_id = user_item.cleaned_data["item_id"]
        user_id = user_item.cleaned_data["user_id"]
        if request.user.id != user_id:
            return False
        return {'object_id' : object_id, 'user_id': user_id}
    else: 
        return False

def fetch_listing_by_id(id):
        
    try:
        listing  = Listings.objects.get(pk = id)
    except Listings.DoesNotExist:
        return False
    return listing

def watchlisted_check(user, object_id):

    try:
        user.watchlisted.get(pk = object_id)
        return True
    except Listings.DoesNotExist: 
        return False
    
def list_opener_check(user_id, object_id):

    item = fetch_listing_by_id(object_id)
    user_of_listing = item.object_lister
    if (user_of_listing.id) == user_id:
        return True
    return False
    
def calculate_current_highest_bid(id):
    highest_bid_item = Bids.objects.filter(object_id=id).order_by('-bid_amount').first()

    if not highest_bid_item:
        current_price = fetch_listing_by_id(id).object_price
    else:
        current_price = highest_bid_item.bid_amount

    return current_price

def find_winner_by_id(item_id):

    item = fetch_listing_by_id(item_id)

    if item.listing_open:
        return False

    highest_bid_item = Bids.objects.filter(object_id=item_id).order_by('-bid_amount').first()

    if not highest_bid_item:
        return item.object_lister
    else:
        return highest_bid_item.bidder_id

def check_winner(user_id, item_id):

    item_winner = find_winner_by_id(item_id)
    if item_winner:
        if item_winner.id == user_id:
            return True
    return False