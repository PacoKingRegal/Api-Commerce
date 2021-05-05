import requests
from requests.auth import HTTPBasicAuth
import xmltodict

WEBSERVICE_KEY = "K23MFEIG5L7C41U3LNY377JNC9WV1UDE"

params = {}

url = "http://lafabricadegolosinas.com/api/?ws_key=K23MFEIG5L7C41U3LNY377JNC9WV1UDE"

url = "http://lafabricadegolosinas.com/api/carts/?ws_key=K23MFEIG5L7C41U3LNY377JNC9WV1UDE"
url = "http://lafabricadegolosinas.com/api/orders/4464?ws_key=K23MFEIG5L7C41U3LNY377JNC9WV1UDE"



'''
response = requests.get(url, params=params)
content = response.content

doc_json = xmltodict.parse(content)


lineas = []
for elem in doc_json["prestashop"]["order"]["associations"]["order_rows"]["order_row"]:
    
    linea = {}
    linea["id"] = elem["id"]
    linea["product_quantity"] = elem["product_quantity"]
    linea["product_reference"] = elem["product_reference"]
    linea["product_price"] = elem["product_price"]
    linea["product_name"] = elem["product_name"]

    lineas.append(linea)

    
print(lineas)

for linea in lineas:
    print(linea["id"])

'''



'''
url = "http://lafabricadegolosinas.com/api/stock_availables/?ws_key=K23MFEIG5L7C41U3LNY377JNC9WV1UDE"



response = requests.get(url, params=params)
content = response.content

print(content)

doc_json = xmltodict.parse(content)

print(doc_json)

for elem in doc_json["prestashop"]["stock_availables"]['stock_available']:
    #linea = {}
    print(elem)
    #linea["id"] = elem["id"]
    #linea["product_quantity"] = elem["product_quantity"]
    #linea["product_reference"] = elem["product_reference"]
    #linea["product_price"] = elem["product_price"]
    #linea["product_name"] = elem["product_name"]

    #lineas.append(linea)

'''


    




url = "http://lafabricadegolosinas.com/api/products/?display=full&output_format=XML&ws_key=K23MFEIG5L7C41U3LNY377JNC9WV1UDE"

url2 = "http://lafabricadegolosinas.com/api/products/?display=full&output_format=XML"
key = "K23MFEIG5L7C41U3LNY377JNC9WV1UDE"

#response = requests.get(url, params=params )
response = requests.get(url2, auth=(key, ''), params=params )
print(response.status_code)

content = response.content


doc_json = xmltodict.parse(content)

articulos = []

for elem in doc_json["prestashop"]["products"]["product"]:
    
    try:    
        articulo = {}
    
        articulo['id_articulo'] = elem['id']
        articulo['rererence'] = elem['reference']
        articulo['id_categoria'] = elem['id_category_default']['@xlink:href']
        articulo['texto'] = elem['id_category_default']['#text']
        articulo['supplier_reference'] = elem['supplier_reference']
        articulo['descuento_cantidad'] = elem['quantity_discount']
        articulo['ean13'] = elem['ean13']
        articulo['estado'] = elem['state']
        articulo['en_venta'] = elem['on_sale']
        articulo['solo_online'] = elem['online_only']
        articulo['ecotax'] = elem['ecotax'] 
        articulo['cantidad_minima'] = elem['minimal_quantity']
        articulo['aviso_stock_bajo'] = elem['low_stock_alert']
        articulo['precio'] = elem['price']
        articulo['mostrar_precio'] = elem['show_price']
        articulo['fecha_alta'] = elem['date_add']
        articulo['fecha_ultima_modificacion'] = elem['date_upd']
        articulo['pack_stock_type'] = elem['pack_stock_type']
        articulo['meta_descripcion'] = elem['meta_description']['language']['#text']
        articulo['meta_keywords'] = elem['meta_keywords']['language']['#text']
        articulo['meta_title'] = elem['meta_title']['language']['#text']
        articulo['link_rewrite'] = elem['link_rewrite']['language']['#text']
        articulo['nombre'] = elem['name']['language']['#text']
        articulo['descripcion'] = elem['description']['language']['#text']
        articulo['descripcion_short'] = elem['description_short']['language']['#text']
        
        #assosiations
        articulos.append(articulo)
        
    except:
        pass
        

for articulo in articulos:
    print(articulo)
    

