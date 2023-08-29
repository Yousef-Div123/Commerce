from email.policy import default
from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models



class Category(models.Model):
    option = models.CharField(max_length=32)
    listings = models.ManyToManyField("Listing", blank=True)

    def __str__(self):
        return f"{self.option}"

class Comments(models.Model):
    user =  models.ForeignKey("User", on_delete=models.CASCADE, null =True)   
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="comment_listing", null=True)  
    content = models.TextField(blank = True) 

    def __str__(self):
        return f"{self.listing}"    

class Listing(models.Model):
    title = models.CharField(max_length=64 )
    description = models.TextField()
    starting_bid = models.PositiveIntegerField()
    listing_category = models.ManyToManyField(Category, blank=True, related_name="category")
    user = models.ForeignKey("User", blank=True, on_delete= models.CASCADE, null=True)
    comments = models.ManyToManyField(Comments, blank = True, related_name="listing_comment")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"

class User(AbstractUser):
    watchlist = models.ManyToManyField(Listing , blank=True, related_name="watchlist")

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    biders = models.ManyToManyField(User, blank = True)
    last_bidder = models.ForeignKey(User, blank= True, on_delete = models.CASCADE, related_name="last_bidder", null=True)    

    def __str__(self):
        return f"{self.listing.title}"


