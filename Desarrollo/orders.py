#!/usr/bin/env python3
from requests.api import get
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

def get_orders( status="processing"):
    '''
    status = (pending, processing, on-hold, completed, cancelled, refunded, failed and trash)
    '''
    orders = wcapi.get('orders',params={"per_page": 100, "page": 1, "offset": 0}).json()
    print(orders)
    orders_list = []
    for order in orders:
        order_dict = {}
        order_dict["id"] = order["id"]
        order_dict["number"] = order["number"]
        order_dict["status"] = order["status"]
        order_dict["date_created"] = order["date_created"]
        
        order_dict["productos"] = []
        for linea in order["line_items"]:
            linea_dict = {}
            linea_dict["id"] = linea["id"]
            linea_dict["sku"] = linea["sku"]
            linea_dict["name"] = linea["name"]
            linea_dict["quantity"] = linea["quantity"]
            order_dict["productos"].append(linea_dict)
    
        if order_dict["status"] == status:
            orders_list.append(order_dict)
            

    '''
    if status != "":
        return [d for d in orders_list if d["status"] == status]
    '''
    
    return orders_list

def fichero_to_json(json_f="sample.json"):
    '''
        Params: json_f: Nombre del ficher json en el que guardaremos la información. 
                        Contiene un valor por defecto en caso de no introducir nada
    '''
    lista = get_orders()
    with open(json_f, "w") as outfile:
        json.dump(lista, outfile, separators=(',', ':'))

def change_status(status, id_order):
    '''
        Params: status: Estado al que actualizamos el pedido
                id_order: Id del pedido que vamos a actualizar
    '''
    print(wcapi.put("orders/"+id_order, data={"status": status}).json())

def delete_order(id_order):
    '''
        Params: id_order: Id del pedido que vamos a eliminar
    '''
    print(wcapi.delete("orders/"+id_order , params={"force": True}).json())

def create_order():
    data = {
        "payment_method": "bacs",
        "payment_method_title": "Direct Bank Transfer",
        "set_paid": True,
        "billing": {
            "first_name": "Prueba",
            "last_name": "Python Add",
            "address_1": "969 Market",
            "address_2": "",
            "city": "San Francisco",
            "state": "CA",
            "postcode": "94103",
            "country": "US",
            "email": "john.doe@example.com",
            "phone": "(555) 555-5555"
        },
        "shipping": {
            "first_name": "Prueba",
            "last_name": "Python Add",
            "address_1": "969 Market",
            "address_2": "",
            "city": "San Francisco",
            "state": "CA",
            "postcode": "94103",
            "country": "US"
        },
        "line_items": [
            {
                "product_id": 629,
                "quantity": 8
            },
        ],
        "shipping_lines": [
            {
                "method_id": "flat_rate",
                "method_title": "Flat Rate",
                "total": "8.00"
            }
        ]
    }

    print(wcapi.post("orders", data).json())

'''
for order in get_orders(status="processing"):
    print(order)

'''

#Guardar todos los pedidos en un JSON
#print(fichero_to_json(json_f="pruebanueva.json"))

#Cambio estado de un pedidio (En proceso...)
#change_status(status="cancelled", id_order="3041")

#Borrar un pedido 
#delete_order(id_order="3041")

#Crear un pedido
#create_order()





