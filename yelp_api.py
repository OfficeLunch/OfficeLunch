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

def get_search(location):
    params = {
        'term' : 'restaurants',
        'lang' : 'en',
        'limit': 20,
        'radius_filter' : 8000,
        'sort' : 2
    }

    response = client.search_by_coordinates(location['lat'],location['long'], **params)
    #for x in response.businesses:
        #print '%-*s%s%f%f' % (35, x.name, x.categories,x.location.coordinate.latitude,x.location.coordinate.longitude)
    return response
