from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("closed_listings", views.closed_listings, name="closed"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("item/<int:id>", views.show_item, name = "show_item"),
    path("change_watchlist", views.change_watchlist, name="change_watchlist"),
    path("place_bid", views.place_bid, name="place_bid"),
    path("close_listing", views.close_listing, name="close_listing"),
    path("post_comment", views.post_comment, name="post_comment"),
    path("watchlisted", views.watchlisted, name="watchlisted"),
    path("category_list", views.category_list, name="category_list"),
    path("category/<int:category>", views.category, name="category"),
]
