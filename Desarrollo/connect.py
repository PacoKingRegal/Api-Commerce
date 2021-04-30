#!/usr/bin/env python3
from woocommerce import API
import json


wcapi = API(
  url="https://krdrinks.eu",
  consumer_key="ck_0d4cca94752e3bad9196767981098c88c73a7662",
  consumer_secret="cs_42e5c11402e844f5239293ce5fc4122690dca039",
  wp_api = True,
  version = "wc/v3",
  query_string_auth=True
)



#data = { "slug" : "ron-blanco-dale-cana-formato-pet"}

# No modifica precio
data = { "price" : "0.95"}

a = wcapi.put("products/1999", data)

#print(a.json())
product = wcapi.get('products/1999').json()
print(product.keys())
print(product["id"])
print(product["price"])

print(product["slug"])


#elem = [i for i in response if i["id"] == 1999]
#print(elem)
'''
'''
response = wcapi.get('products').json()


dict1 = {}




for elem in response:
    print('-----------')
    #print(elem)
    print('El id es: ' + str(elem["id"]))
    print(elem["name"])
    print(elem["price"])
    print(elem["regular_price"])

    print(elem["slug"])
    dict1['clave'] = elem["id"]
    dict1['precio'] = elem["price"]

print(dict1)


for i, v in dict1.items():
    print(i, v)
'''
    
#print(elem["permalink"])


'''
orders = wcapi.get('orders').json()
print(orders)
'''
