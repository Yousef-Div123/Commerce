from xml.etree.ElementTree import Comment
from django.contrib import admin
from .models import Bid, Listing, Category, User, Comments

# Register your models here.

admin.site.register(Listing)
admin.site.register(Comments)
admin.site.register(Bid)
admin.site.register(Category)
