from django import forms
from WebUAuctionSearch.models import AuctionSiteDetails, Search

class SearchForm(forms.ModelForm):
    reference = forms.CharField(max_length=20, 
                            help_text="Own reference for search results, Not compulsary", 
                            required=False)
    description = forms.CharField(max_length=128, 
                                help_text="Please enter the auction items to be searched for.")
    postcode = forms.CharField(max_length=20,
                                help_text="Postcode or location to look for.") 
    distance = forms.IntegerField(help_text="Distance in miles from postcode.")

    # get each Auction Site defined in databse and populate CheckBox accordingly
    auctionSiteChoices = ()
    for eachAuctionSite in AuctionSiteDetails.objects.all():
        auctionSiteChoices += ((eachAuctionSite.name, eachAuctionSite.caption), )  

    auction_Choices = forms.MultipleChoiceField(
                                                required=True,
                                                widget=forms.CheckboxSelectMultiple,
                                                choices=auctionSiteChoices
                                                )
    class Meta:
        model = Search
        fields = ('reference', 'description', 'postcode', 'distance','auction_Choices')