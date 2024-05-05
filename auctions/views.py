from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import NewListingForm, Item_user_combo, CommentsForm
from .models import User, Listings, Bids
from .utils import check_post_method, login_required, process_user_item_combo, fetch_listing_by_id, watchlisted_check, calculate_current_highest_bid, list_opener_check, check_winner


def index(request):

    active_listings = Listings.objects.all().filter(listing_open = True)

    return render(request, "auctions/index.html" , {
        "listings" : active_listings,
        "status": "Active"
    })

def closed_listings(request):

    closed_listings = Listings.objects.all().filter(listing_open = False)

    return render(request, "auctions/index.html" , {
        "listings" : closed_listings,
        "status": "Closed"
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone_number"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, phone_number = phone)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):

    if request.method == "POST":

        listingform = NewListingForm(request.POST)
        if listingform.is_valid():

            listingform["object_lister"] = request.user
            listingform.save()

        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create_listing.html", {
        'form': NewListingForm()
    })

@login_required
def show_item(request, id):
    
    listing  = fetch_listing_by_id(id)

    if not listing: 
        return render(request, "auctions/error_page.html", {
        'error_message': 'Listing not found'
    })

    user = request.user

    watchlisted_item = watchlisted_check(user, id)

    object_user = Item_user_combo(initial={
        'item_id': id,
        'user_id': user.id
        })

    current_price = calculate_current_highest_bid(id)

    owner_check = list_opener_check(user.id, id)
    winner_check = check_winner(user.id, id)

    comment_form = CommentsForm()

    return render(request, "auctions/listing_page.html", {
        'item': listing,
        'watch_listed': watchlisted_item,
        'current_bid': current_price,
        'object_user': object_user,
        'owner_check': owner_check,
        'winner_check': winner_check,
        'comment_form': comment_form
    })

@check_post_method
def change_watchlist(request):

    user_items = process_user_item_combo(request)

    if not user_items:
        return HttpResponseRedirect(reverse("index"))

    action = request.POST["action"]

    user = get_object_or_404(User, pk = user_items["user_id"])
    Watchlisted_item = Listings.objects.get(pk = user_items["object_id"])

    if action == "add":
        user.watchlisted.add(Watchlisted_item)
    if action == "remove":
        user.watchlisted.remove(Watchlisted_item)
    user.save()

    return HttpResponseRedirect(reverse("show_item", kwargs={"id": user_items["object_id"]}))

@login_required
@check_post_method
def place_bid(request):

    user_items = process_user_item_combo(request)
    user = get_object_or_404(User, pk = user_items["user_id"])

    object_id = user_items["object_id"]
    item = fetch_listing_by_id(object_id)
    
    bid_amount = float(request.POST["bid_amount"])

    if bid_amount <= calculate_current_highest_bid(object_id):
        return render(request, "auctions/error_page.html", {
            'error_message': 'Bid amount lower than current bid, try again'
        })

    new_bid = Bids(object_id = item, bid_amount = bid_amount, bidder_id = user)
    new_bid.save()

    return HttpResponseRedirect(reverse("show_item", kwargs={"id": object_id}))

@check_post_method
def close_listing(request):

    user_items = process_user_item_combo(request)

    id = user_items["object_id"]
    user_id = user_items["user_id"]

    owner_check = list_opener_check(user_id, id)
    if not owner_check:
        return render(request, "auctions/error_page.html", {
            'error_message': 'You are not the owner of this listing'
        })

    listing = fetch_listing_by_id(id)
    listing.listing_open = False

    listing.save()

    return HttpResponseRedirect(reverse("show_item", kwargs={"id": id}))