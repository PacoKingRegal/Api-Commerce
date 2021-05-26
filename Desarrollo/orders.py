#!/usr/bin/env python3
from woocommerce import API
import json
import pandas as pd


wcapi = API(
  url="https://krdrinks.eu",
  consumer_key="ck_0d4cca94752e3bad9196767981098c88c73a7662",
  consumer_secret="cs_42e5c11402e844f5239293ce5fc4122690dca039",
  wp_api = True,
  version = "wc/v3",
  query_string_auth=True
)


def fichero_to_json(json_f="sample.json", lista=""):
    with open(json_f, "w") as outfile:
        json.dump(lista, outfile, separators=(',', ':'))

def get_orders( status=""):
    '''
    status = (pending, processing, on-hold, completed, cancelled, refunded, failed and trash)
    '''
    orders = wcapi.get('orders',params={"per_page": 100, "page": 1, "offset": 0}).json()
    print(orders)
    orders_list = []
    for order in orders:
        order_dict = {}
        order_dict["number"] = order["number"]
        order_dict["status"] = order["status"]
        order_dict["date_created"] = order["date_created"]
        
        order_dict["productos"] = []
        for linea in order["line_items"]:
            linea_dict = {}
            linea_dict["id"] = linea["id"]
            linea_dict["sku"] = linea["sku"]
            linea_dict["quantity"] = linea["quantity"]
            order_dict["productos"].append(linea_dict)
            

        orders_list.append(order_dict)

    if status != "":
        return [d for d in orders_list if d["status"] == status]
    
    '''
    df = pd.DataFrame.from_dict(orders_list)
    df.to_excel("pedidos_wc.xlsx")
    '''
    fichero_to_json(lista=orders_list)
    return orders_list


for order in get_orders():
    print(order)

for order in get_orders(status="completed"):
    print(order)



