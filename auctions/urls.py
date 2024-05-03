from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("item/<int:id>", views.show_item, name = "show_item"),
    path("change_watchlist", views.change_watchlist, name="change_watchlist"),
    path("place_bid", views.place_bid, name="place_bid"),
]
