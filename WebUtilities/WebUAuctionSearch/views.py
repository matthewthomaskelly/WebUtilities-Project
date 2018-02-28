'''
'''
import ast # use ast to evaluate json item stored as text in DB 

from django.shortcuts import render
# forms and models
from WebUAuctionSearch.forms import SearchForm
from WebUAuctionSearch.models import AuctionSiteDetails, UrlProxy

# user defined class WebAuctionSoup to build URL search parameters, get request, soup and subsequently scrape soup item...
from WebUAuctionSearch.modules.WebAuctionSoup import WebAuctionSoup

'''
Standard index page. Plain HTML at present
'''
# Create your views here.
def index(request):
    # this is the view
    return render(request, 'index.html')


'''
Nothing at present, but intended to be informative hanging token
'''
def right(request):
    return render(request, 'right.html')


'''
Form where search criteria are entered and either displayed or results processed using BS4
'''
def new_search(request):

    # this is the view
    form = SearchForm()
    if request.method == 'POST':
        # grab the data from the submitted form
        form = SearchForm(data=request.POST)

    # process away...
    if form.is_valid():

        # create an empty return dictionary for HTML rendering
        itemsDic = {}

        # at present only description, distance, postcode...
        description = form.cleaned_data['description']
        distance = str(form.cleaned_data['distance'])
        postcode = form.cleaned_data['postcode']
        #  ...and auction choices are used to search auction sites.

        # loop for each selection and each choice in DB
        for eachWebsiteChoice in form.cleaned_data['auction_Choices']:
            for eachDBAuctionSite in AuctionSiteDetails.objects.all():

                # search only web auction sites selected
                if eachWebsiteChoice in eachDBAuctionSite.name:

                    # What is the current website search URL? (different for some, e.g. ebay)
                    webSearchAddress = eachDBAuctionSite.url_search

                    # get query terms items and substitute chosen search term values
                    queryTerms = eachDBAuctionSite.queryTermsDic
                    queryTerms = queryTerms.replace('@description', description)
                    queryTerms = queryTerms.replace('@distance', distance)
                    queryTerms = queryTerms.replace('@postcode', postcode)
                    queryTerms = ast.literal_eval(queryTerms)

                    # Then obtain Soup search terms for resultant website structure 
                    soupTerms = eachDBAuctionSite.soupTermsDic
                    soupTerms = ast.literal_eval(soupTerms)

                    # each auction site will have its own dictionary key items...
                    itemsDic[eachDBAuctionSite.name] = {}
                    # ...go get 'em!
                    itemsDic[eachDBAuctionSite.name] = get_items_dic(webSearchAddress, queryTerms, soupTerms)

                    # User input reference will be used a heading
                    reference = form.cleaned_data['reference']
                    # followed by search term criteria as sub-heading
                    searchCriteria = description + " within " + distance + " miles of " + postcode

        # return to the results page
        return render(request, 'results.html', {'items_dic': itemsDic, 'reference': reference, 'searchCriteria': searchCriteria} )
    else:
        print(form.errors)

    # return the search form
    return render(request, 'search.html', {'form': form,})


'''
Function to return items dictionary that will be sent back to django render for results page
'''
def get_items_dic(webSearchAddress, queryTerms, soupTerms):

    # Get object instance of WebAuctionSoup
    AuctionsResultsSoup = WebAuctionSoup()

    # from web (Search) address and query terms, build url query with search parameters
    urlRequest = AuctionsResultsSoup.create_url_request(webSearchAddress, queryTerms)

    # get each Proxy from Proxys DB object
    for eachProxy in UrlProxy.objects.all():
        # assign to 
        Proxies = {
                    'http': eachProxy.httpProxy,
                    'https': eachProxy.httpsProxy
                }
        # ...and try and get Soup
        try:
            resultsSoup = AuctionsResultsSoup.get_soup(urlRequest, Proxies)
            break
        except:
            print("Exception, in obtaining results Soup!")
    else:
        # if no Proxies and/or Proxies failed. Use default
        resultsSoup = AuctionsResultsSoup.get_soup(urlRequest)

    # We should have Soup by this point.
    # Set an empty dictionary to return or add list items to for django rendering    
    returnDic = {}
    # want first element of dictionary to be heading and list of elements scraped from auction site
    returnDic.update({str(0): soupTerms['elements'] })

    # enumerate through each listing recovered from Soup
    try:
        for index, currentItem in enumerate(AuctionsResultsSoup.get_website_items_dict(resultsSoup, soupTerms) ):
            returnDic.update({str(index+1): currentItem })
    except:
        # set return dictionary element to Zilch on failure
        returnDic.update({str(index+1): {} })

    return returnDic