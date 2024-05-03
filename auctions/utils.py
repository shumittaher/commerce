from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import Item_user_combo
from .models import Listings
from django.shortcuts import render



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
        return {'object_id' : object_id, 'user_id': user_id}
    
    else: 
        return False

def fetch_listing_by_id(id):
        
    try:
        listing  = Listings.objects.get(pk = id)
    except Listings.DoesNotExist:
        return False
    return listing
