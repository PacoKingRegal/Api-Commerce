#!/usr/bin/env python3
from woocommerce import API
import xmltodict
import pandas as pd
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
'''
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


def fichero_to_json(json_f="sample.json", lista=""):
    with open(json_f, "w") as outfile:
        json.dump(lista, outfile, separators=(',', ':'))

response = wcapi.get('products',params={"per_page": 70, "page": 1, "offset": 0}).json()
print(response)

productos = []




for elem in response:
    producto = {}

    producto["id"] = elem["id"]
    producto["name"] = elem["name"]
    producto["price"] = elem["price"]
    producto["regular_price"] = elem["regular_price"]
    productos.append(producto)

fichero_to_json(json_f="productos_wc.json",lista=productos)
print(productos)


'''

#print(elem["permalink"])

orders = wcapi.get('orders').json()
print(orders)

'''
