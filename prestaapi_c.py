#from importlib import metadata
#from prestapyt import PrestaShopWebServiceError, PrestaShopWebService

from prestashop_api import PrestashopApi

WEBSERVICE_KEY = "K23MFEIG5L7C41U3LNY377JNC9WV1UDE"
URL = "http://lafabricadegolosinas.com/api"



# Careful, api calls raise PrestashopError if request fails
api = PrestashopApi(URL, WEBSERVICE_KEY)
print(api)

res = api.get('adresses')
print(res)

for p in res['products']['product']:
    print(p['@id'], p['@xlink:href'])

'''
from prestapyt import PrestaShopWebService

WEBSERVICE_KEY = "K23MFEIG5L7C41U3LNY377JNC9WV1UDE"
URL = "http://LAFABRICADEGOLOSINAS.com"
prestashop = PrestaShopWebService(URL, WEBSERVICE_KEY)
'''

'''
from prestapyt import PrestaShopWebServiceDict

WEBSERVICE_KEY = "K23MFEIG5L7C41U3LNY377JNC9WV1UDE"
URL = "http://LAFABRICADEGOLOSINAS.com"
prestashop = PrestaShopWebServiceDict(URL, WEBSERVICE_KEY)
'''
