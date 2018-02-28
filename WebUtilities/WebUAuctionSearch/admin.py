from django.contrib import admin

# Register your models here.
from WebUAuctionSearch.models import AuctionSiteDetails, UrlProxy

admin.site.register(AuctionSiteDetails)
admin.site.register(UrlProxy)