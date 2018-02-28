from django.db import models

'''
Search - model for supported items in search form...
'''
class Search(models.Model):
    reference = models.CharField(max_length=20)
    description = models.CharField(max_length=128)
    postcode = models.CharField(max_length=9)
    distance = models.IntegerField()

    def __str__(self):
        return self.reference

'''
AuctionSiteDetails - model for Search parameter URL make-up and subsequent results scraping details
'''
class AuctionSiteDetails(models.Model):
    name = models.CharField(max_length=30)
    caption = models.CharField(max_length=30) 
    url_site = models.CharField(max_length=30) 
    url_search = models.CharField(max_length=30) 
    queryTermsDic = models.CharField(max_length=256)
    soupTermsDic = models.CharField(max_length=256)
    
    def __str__(self):
        return self.name

'''
UrlProxy - model to store a number of UK proxies to try for UK based results
'''
class UrlProxy(models.Model):
    urlName = models.CharField(max_length=30)
    httpProxy = models.CharField(max_length=30)
    httpsProxy = models.CharField(max_length=30)

    def __str__(self):
        return self.urlName