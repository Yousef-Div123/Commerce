from optparse import Option
from pydoc import describe
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Bid, User, Listing, Category, Comments


def index(request):
    return render(request, "auctions/index.html", {
        "listings" : Listing.objects.order_by('-active', 'pk')
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

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url= "login")
def add(request):
    if request.method == "POST":
        try:
            title = request.POST["title"]
            try:
                Listing.objects.get(title = title) 
                return render(request, "auctions/add.html" , {
                    "categories" : Category.objects.all(),
                    "error_message": "Error: the title is already taken"
                })
            except:
                description = request.POST["description"]
                bid = request.POST["bid"]
                if int(bid) < 0:
                        return render(request, "auctions/add.html" , {
                            "categories" : Category.objects.all(),
                            "error_message": "Error: Starting bid can't be in minus"
                        }) 
                category = Category.objects.get(pk = request.POST["category"])
                user = request.user
                listing = Listing( title = title, description = description, starting_bid = bid, user = user)
                listing.save()
                listing.listing_category.add(category)
                category.listings.add(listing)

                #bid
                listing_bid = Bid(listing = listing)
                listing_bid.save()
                return render(request, "auctions/index.html", {
                "listings" : Listing.objects.order_by('-active', 'pk')
                })
        except ValueError:
            return render(request, "auctions/add.html" , {
                "categories" : Category.objects.all(),
                "error_message": "Error: You have to fill all of the empty places"
            })
                
    return render(request, "auctions/add.html" , {
        "categories" : Category.objects.all()
    })

def listing(request, listing_title):
    try:
        listing = Listing.objects.get(title = listing_title)
        bid = Bid.objects.get(listing = listing)
        comments = listing.comments.all()
        user = User.objects.get(username = request.user)
        in_watchlist = False
        
        if user.watchlist.filter(title = listing.title):
            in_watchlist = True

        if in_watchlist:
            watchlist_message = "Remove from watchlist"
        else:
            watchlist_message = "Add to watchlist"  
        if request.method == "POST":
            if "watchlist" in request.POST: 
                if in_watchlist == False:
                    user.watchlist.add(listing)
                    return render(request, "auctions/watchlist.html", {
                        "listings": user.watchlist.all()
                    })
                else:
                    user.watchlist.remove(listing)
                    return render(request, "auctions/watchlist.html", {
                        "listings": user.watchlist.all()
                    })
            elif "bid" in request.POST:
                if bid.biders.count() == 0:
                    if int(request.POST["bid"]) >= int(listing.starting_bid):
                        listing.starting_bid = int(request.POST["bid"])
                        bid.last_bidder = request.user
                        bid.biders.add(request.user)
                        listing.save()
                        bid.save()

                    else:
                        return render(request, "auctions/listing.html", {
                            "listing" : listing,
                            "comments": comments,
                            "categories": listing.listing_category.all(),
                            "watchlist_message": watchlist_message,
                            "error_message": "Error: Your bid must be higher than or equal to the current price"
                        }) 
                else:
                    if int(request.POST["bid"]) > int(listing.starting_bid):
                        listing.starting_bid = int(request.POST["bid"])
                        bid.last_bidder = request.user
                        bid.biders.add(request.user)
                        listing.save()
                        bid.save()

                    else:
                        return render(request, "auctions/listing.html", {
                            "listing" : listing,
                            "comments": comments,
                            "categories": listing.listing_category.all(),
                            "watchlist_message": watchlist_message,
                            "error_message": "Error: Your bid must be higher than the last bid"
                        })           
            elif "close bid" in request.POST:
                listing.active = False
                listing.save()                 

            elif "comment" in request.POST:
                content = request.POST["content"]
                if content == "":
                    return render(request, "auctions/listing.html", {
                        "listing" : listing,
                        "comments": comments,
                        "categories": listing.listing_category.all(),
                        "watchlist_message": watchlist_message,
                        "error_message": "Error: Your comment mustn't be empty"
                    })   
                comment = Comments(user = user, listing = listing ,content = content)
                comment.save()
                listing.comments.add(comment)
                listing.save()
                return render(request, "auctions/listing.html", {
                    "listing" : listing,
                    "comments": comments,
                    "categories": listing.listing_category.all(),
                    "watchlist_message": watchlist_message,
                })

            
        return render(request, "auctions/listing.html", {
            "listing" : listing,
            "bid": bid,
            "comments": comments,
            "categories": listing.listing_category.all(),
            "watchlist_message": watchlist_message
        })
    except:
        return render(request, "auctions/listing.html", {
            "listing" : listing,
            "bid": bid,
            "comments": comments,
            "categories": listing.listing_category.all()
        })



@login_required(login_url= "login")
def watchlist(request):
    user = User.objects.get(username = request.user) 
    watchlist = user.watchlist.order_by('-active')
    return render(request, "auctions/watchlist.html", {
        "listings": watchlist
    })

def category(request):
    return render(request, "auctions/category.html", {
        "categories": Category.objects.all()
    })  

def category_listing(request, category):
    category = Category.objects.get(option = category)
    listings = category.listings.filter(active=True)
    if not listings:
        empty = False
    else:
        empty = True    
    return render(request, "auctions/category_listing.html", {
        "category": category,
        "listings":listings,
        "empty": empty
    })    

@login_required(login_url= "login")
def my_listings(request):
    
    #my own listings
    
    listings = Listing.objects.filter(user = request.user)
    if not listings:
        empty_listings = True
    else:
        empty_listings = False    


        

    #listings that I won
    
    bids = Bid.objects.filter(last_bidder = request.user, listing__active = False)
    if not bids:
        empty_bids = True    
    else:
        empty_bids = False

    #bids which I have joined
    joined_bids = Bid.objects.filter(biders = request.user)
    if not joined_bids:
        empty_joined_bids = True
    else:
        empty_joined_bids = False    


    return render(request, 'auctions/my_listings.html', {
        "listings" : listings,
        "empty_listings" : empty_listings,
        "empty_bids": empty_bids,
        "empty_joined_bids" : empty_joined_bids,
        "joined_bids" : joined_bids,
        "bids": bids
    })    