import io, json, time, logging

from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

formatting = '%(asctime)-15s %(message)s'
#logging.Formatter.converter = time.gmtime
#logging.basicConfig(filename=r'yelp_testing.log', format=formatting, level=logging.INFO)

# read API keys from config file
with io.open('config.json') as cred:
    creds = json.load(cred)
    auth = Oauth1Authenticator(**creds)
    client = Client(auth)

#takes a dictionary with lat/long and returns a response object (with 20 restaurants)
def get_search(location):
    params = {
        'term' : 'restaurants',
        'lang' : 'en',
        'limit': 20,
        'radius_filter' : 8000,
        'sort' : 2
    }

    response = client.search_by_coordinates(location['lat'],location['long'], **params)
    return response

#as above but returns 2 responses with 20 each
def get_search40(location):
    params = {
        'term' : 'restaurants',
        'lang' : 'en',
        'limit': 20,
        'radius_filter' : 8000,
        'sort' : 2
    }

    response1 = client.search_by_coordinates(location['lat'],location['long'], **params)
    params['offset'] = 20
    response2 = client.search_by_coordinates(location['lat'],location['long'], **params)

    return [response1, response2]

#takes a yelp response and a list of tags and will return a list of 10 restaurants(dictionaries)
def sortRestaurants(metatags,response):
    metaList = {}
    listofBusiness = []
    weightList = {}
    for tag in metatags:
        if not tag in metaList:
            metaList[tag] = 1
        else:
            metaList[tag] += 1

    print metaList

    for x in response.businesses:
        #print x.categories
        for key in metaList:
            #print key
            for cats in x.categories:
                for tag in cats:
                    if tag in key:
                        #print key
                        listofBusiness.append(x)

    #print listofBusiness
    for dictionary in listofBusiness:
        #print dictionary.name
        for listCategories in dictionary.categories:
            if not dictionary.name in weightList:
                weightList[dictionary.name] = 1
            else:
                weightList[dictionary.name] += 1

    maximum = 0
    for i in listofBusiness:
        if weightList[i.name] > maximum:
            maximum = weightList[i.name]
            listofBusiness.insert(0,listofBusiness.pop(listofBusiness.index(i)))

    return listofBusiness[:10]
