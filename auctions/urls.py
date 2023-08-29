from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add, name="add"),
    path("listings/<str:listing_title>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name = "watchlist"),
    path("categories", views.category, name="category"),
    path("categories/<str:category>", views.category_listing, name="category_listing"),
    path("My listing", views.my_listings, name="my_listings")
]

