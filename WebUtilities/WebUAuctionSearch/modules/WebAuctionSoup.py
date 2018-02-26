import bs4 # beautiful soup
import urllib.request # url library to request an url
import urllib.parse # url library to parse htmk queries


# ************************************************************************
# ** Name:          Class WebAuctionSoup()
# ** Purpose:       To take a list of values and to scrape websites for items as
# **                 specified. Examples include GumTree.com bike, within radius 
# **                 of a postcode.
# ****          This class will currently only handle GumTree searches.         ****
# ****          Use Inheritance for further websites such as eBay, Preloved?    ****    
# ** Creation date: March 2017
# ** Author:        Matthew KELLY
# ** Inputs:        None at present
# ** Returns:       None at present
# ** Amendments:    June 2017 - changed code for BS4 and URL request into Class...
# ************************************************************************
class WebAuctionSoup():

    # when an image is downloaded, this will be temporarily saved in the following
    #  variable until a further download is successfully completed
    CurrentDownloadedImageFileName = ""

    # ********************************************************************
    # ** Name:      create_url_request
    # ** Purpose:   Takes Website URL and Specified SearchItems
    # ** Inputs:    WebsiteUrl website for search, and
    # **            dictionary of SearchTerms
    # ** Returns:   URL search term
    # ** Amendments:None
    # ********************************************************************
    def create_url_request(self, WebsiteUrl, SearchItems):

        # using urlib.parse create query instruction from dictionary of search terms
        Query = urllib.parse.urlencode(SearchItems)

        # create list of items for full url creation
        WebsiteUrl =("https", WebsiteUrl, "search", Query, "")

        # create full url request from specified terms as above
        UrlRequest = urllib.parse.urlunsplit(WebsiteUrl)

        return UrlRequest

    # ********************************************************************
    # ** Name:      function get_website_items_dict
    # ** Purpose:   Queries the Soup item to return specific items
    # **            This is the class function that would mainly need amending 
    # **             if other websites were incorporated
    # ** Inputs:    soup - current soup item
    # **            RelativeFolderToDownload - optional folder location to save images
    # ** Returns:   List of items located
    # ** Amendments:None at present
    # ********************************************************************
    def get_website_items_dict(self, soup, websiteDict):

        # does it have a findAll:
        if 'findAll' in websiteDict:
            # find all natural soup items
            FindAllSoupItems = soup.find_all(class_=websiteDict['findAll'])
        else: # just continue 
            FindAllSoupItems = soup

         # iterate through each 'natural' item pulling specified data and storing this in variables    
        for CurrentSoupItem in FindAllSoupItems:

            buildDic = {}

            for eachElement in websiteDict['elements']:

                currString = ""
                try:
                    if eachElement == 'a':
                        # The URL of the Listing (for future reference)
                        currString = CurrentSoupItem.find("a", class_=websiteDict['elements'][eachElement]).get('href')
                        currString = urllib.parse.urljoin(websiteDict['website'], currString)
                    # img
                    elif eachElement == 'img':
                        # get Listing Thumbnail for inclusion in the report
                        for eachDefinition in websiteDict['elements'][eachElement]:
                            currString = CurrentSoupItem.find(class_=eachDefinition[0]).img.get(eachDefinition[1])
                            if currString != None:
                                break
                        if currString == None:    
                            currString = ""
                    else:
                        # The Listing title
                        currString = CurrentSoupItem.find(class_=websiteDict['elements'][eachElement]).get_text()
                except:
                    currString = ""
                #buildDic[eachElement] = currString.strip()
                buildDic[eachElement] = currString
            
            # yield for each natural item
            yield buildDic

    # ********************************************************************
    # ** Name:      function get_soup
    # ** Purpose:   To get SOUP for specicifed URL
    # ** Inputs:    URL for web address to return
    # ** Returns:   Returns Soup
    # ** Amendments:None
    # ********************************************************************
    def get_soup(self, Url):
        # Get request URL
        Req = urllib.request.urlopen(Url)
        # Submit to Beautiful Soup
        Soup = bs4.BeautifulSoup(Req, "html.parser")
        # and return soup
        return Soup

    # ********************************************************************
    # ** Name:      (private) function __download_resource
    # ** Purpose:   To download image from web address
    # ** Inputs:    - UrlToImg - URL to Image we want to download
    # **            - Location path to download image to
    # ** Returns:   None
    # ** Amendments:July 2017 - amended to accept DestinationPathForImg
    # ********************************************************************
    def __download_resource(self, UrlToImg, DestinationPathForImg):
        # open a binary stream for image
        ImgSaveStream = open(DestinationPathForImg, "wb")
        # an try to request image url
        try:
            req = urllib.request.urlopen(UrlToImg)
        except urllib.request.HTTPError as error:
            print(error.code)

        # save this request to the (image) filestream
        ImgSaveStream.write(req.read())

        # tidy up, close both stream and request
        ImgSaveStream.close()
        req.close()