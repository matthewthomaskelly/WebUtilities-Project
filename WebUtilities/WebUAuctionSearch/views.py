import ast

from django.shortcuts import render

from WebUAuctionSearch.forms import SearchForm

from WebUAuctionSearch.models import AuctionSiteDetails

from WebUAuctionSearch.modules.WebAuctionSoup import WebAuctionSoup

# Create your views here.
def index(request):
    # this is the view
    return render(request, 'index.html')

def right(request):
    return render(request, 'right.html')

def new_search(request):

    # this is the view
    form = SearchForm()
    if request.method == 'POST':
        # grab the data from the submitted form
        form = SearchForm(data=request.POST)

    if form.is_valid():

        description = form.cleaned_data['description']
        distance = str(form.cleaned_data['distance'])
        postcode = form.cleaned_data['postcode']

        #form.save(commit=True)
        itemsDic = {}
        
        for eachWebsiteChoice in form.cleaned_data['auction_Choices']:

            for eachDBAuctionSite in AuctionSiteDetails.objects.all():

                if eachWebsiteChoice in eachDBAuctionSite.name: 

                    webSearchAddress = eachDBAuctionSite.url_search

                    queryTerms = eachDBAuctionSite.queryTermsDic
                    queryTerms = queryTerms.replace('@description', description)
                    queryTerms = queryTerms.replace('@distance', distance)
                    queryTerms = queryTerms.replace('@postcode', postcode)
                    queryTerms = ast.literal_eval(queryTerms)

                    soupTerms = eachDBAuctionSite.soupTermsDic
                    soupTerms = ast.literal_eval(soupTerms)
 
                    itemsDic[eachDBAuctionSite.name] = {}                                                          
                    itemsDic[eachDBAuctionSite.name] = get_items_dic(webSearchAddress, queryTerms, soupTerms)
                                
        return render(request, 'results.html', {'items_dic': itemsDic, 'reference': form.cleaned_data['reference']} )
    else:
        print(form.errors)

    return render(request, 'search.html', {'form': form,})
    #return render(request, 'search.html')


def get_items_dic(webSearchAddress, queryTerms, soupTerms):

    AuctionsResultsSoup = WebAuctionSoup()
    urlRequest = AuctionsResultsSoup.create_url_request(webSearchAddress, queryTerms)
    resultsSoup = AuctionsResultsSoup.get_soup(urlRequest)

    returnDic = {}
    returnDic.update({str(0): soupTerms['elements'] })

    try:
        for index, currentItem in enumerate(AuctionsResultsSoup.get_website_items_dict(resultsSoup, soupTerms) ):
            returnDic.update({str(index+1): currentItem })
    except:
        returnDic.update({str(index+1): {} })

    return returnDic