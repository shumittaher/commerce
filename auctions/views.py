from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import NewListingForm
from .models import User, Listings, Bids


def index(request):

    listings = Listings.objects.all()

    return render(request, "auctions/index.html" , {
        "listings" : listings
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

def create_listing(request):

    if request.method == "POST":

        listingform = NewListingForm(request.POST)
        if listingform.is_valid():
            listingform.save()

        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create_listing.html", {
        'form': NewListingForm()
    })


def show_item(request, id):

    if not (request.user.is_authenticated):
        return HttpResponseRedirect(reverse("login"))
    
    try:
        listing  = Listings.objects.get(pk = id)

    except Listings.DoesNotExist:
            return render(request, "auctions/listing_page.html", {
        'error_message': 'Listing not found'
    })       

    try:
        watchlisted_item = request.user.watchlisted.get(pk = id)
    except Listings.DoesNotExist:
        watchlisted_item = None

    highest_bid_price = Bids.objects.order_by('-bid_amount').first()

    if not highest_bid_price:
        current_price = listing.object_price
    else:
        current_price = highest_bid_price

    return render(request, "auctions/listing_page.html", {
        'item': listing,
        'watch_listed': watchlisted_item,
        'current_bid': current_price 
    })

def add_to_watchlist(request):

    if request.method == 'POST':

        object_id = request.POST["object_id"]
        user_id = request.POST["user_id"]

        user = get_object_or_404(User, pk=user_id)
        Watchlisted_item = Listings.objects.get(pk=object_id)

        user.watchlisted.add(Watchlisted_item)
        user.save()

        return HttpResponseRedirect(reverse("show_item", kwargs={"id": object_id}))
    else:
        return HttpResponseRedirect(reverse("index"))
    
def remove_from_watchlist(request):

    if request.method == 'POST':

        object_id = request.POST["object_id"]
        user_id = request.POST["user_id"]

        user = get_object_or_404(User, pk=user_id)
        Watchlisted_item = Listings.objects.get(pk=object_id)

        user.watchlisted.remove(Watchlisted_item)
        user.save()

        return HttpResponseRedirect(reverse("show_item", kwargs={"id": object_id}))
    else:
        return HttpResponseRedirect(reverse("index"))