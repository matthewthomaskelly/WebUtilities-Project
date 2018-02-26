from django.db import models

# Create your models here.
class Search(models.Model):
    reference = models.CharField(max_length=20)
    description = models.CharField(max_length=128)
    postcode = models.CharField(max_length=9)
    distance = models.IntegerField()

    def __str__(self):
        return self.reference

class AuctionSiteDetails(models.Model):
    name = models.CharField(max_length=30)
    caption = models.CharField(max_length=30) 
    url_site = models.CharField(max_length=30) 
    url_search = models.CharField(max_length=30) 
    queryTermsDic = models.CharField(max_length=256)
    soupTermsDic = models.CharField(max_length=256)
    
    def __str__(self):
        return self.name