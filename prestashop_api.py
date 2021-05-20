import requests
import xmltodict
import pandas as pd
import json


class PrestashopApi:
    CORRECT_REQUEST = (200, 201)
        
    def __init__(self, url_base, key):
        self.url_base = url_base
        self.key = key
        
    def get_producto(self, json):
        articulos = []

        if json:
            articulo = {}
            articulo['id_articulo'] = json["prestashop"]["products"]["product"]['id']
            articulo['reference'] = json["prestashop"]["products"]["product"]['reference']
            articulo['id_categoria'] = json["prestashop"]["products"]["product"]['id_category_default']['@xlink:href']
            articulo['ean13'] = json["prestashop"]["products"]["product"]['ean13']
            articulo['precio'] = json["prestashop"]["products"]["product"]['price']
            articulo['peso'] =  json["prestashop"]["products"]["product"]['weight']
            articulo['meta_descripcion'] =  json["prestashop"]["products"]["product"]['meta_description']['language']['#text']
            articulo['meta_keywords'] =  json["prestashop"]["products"]["product"]['meta_keywords']['language']['#text']
            articulo['meta_title'] =  json["prestashop"]["products"]["product"]['meta_title']['language']['#text']
            articulo['nombre'] =  json["prestashop"]["products"]["product"]['name']['language']['#text']
            articulo['descripcion'] =  json["prestashop"]["products"]["product"]['description']['language']['#text']
            articulo['descripcion_short'] =  json["prestashop"]["products"]["product"]['description_short']['language']['#text']
                    
            articulos.append(articulo)
                
            return articulos
        
        else:
            print("No corresponde a ningun articulo")

    def _set_url_request(self, path):
        return self.url_base + '/' + path
    
    def _check_response(self, res):
        if res.status_code not in self.CORRECT_REQUEST:
            print("Error")

    def get_data(self, option):
        '''
            Extraer los datos deseados de la API
            Params: elementos que queremos mostrar (products, order, etc...)
            [id,reference,id_category_default,ean13,price,meta_description,meta_keywords,meta_title,name,description,description_short]
        '''
        url = self.url_base + '/'+ option +'?display=full&output_format=XML&ws_key=' + self.key
        params = {}
        print(url)

        response = requests.get(url, params=params)

        content = response.content
        doc_json = xmltodict.parse(content)
        return doc_json

    def get_filter(self, option, value):
        '''
            Filtro de busqueda de producto
            Params: Option: Elemento de filtrado (ean, referencia, nombre, etc..)
                    Value: Valor del elemento de busqueda
        '''
        url_filter = self.url_base + '/products?display=full&filter['+ option +']=['+ value +']&output_format=XML&ws_key=' + self.key
        params_filter = {}
        print(url_filter)

        response_filter = requests.get(url_filter, params=params_filter)

        content_filter = response_filter.content
        doc_json_by_filter = xmltodict.parse(content_filter)
        return doc_json_by_filter

    def get_products(self, campos=[]):
        doc_json_products = self.get_data(option="products")
        
        articulos = []

        for elem in doc_json_products["prestashop"]["products"]["product"]:
            
            try:  
                #Se han comentado los campos que no se necesitan.  
                articulo = {}
                articulo['id'] = elem['id']
                articulo['reference'] = elem['reference']
                articulo['id_categoria'] = elem['id_category_default']['@xlink:href']
                #articulo['texto'] = elem['id_category_default']['#text']
                #articulo['supplier_reference'] = elem['supplier_reference']
                #articulo['descuento_cantidad'] = elem['quantity_discount']
                articulo['ean13'] = elem['ean13']
                #articulo['estado'] = elem['state']
                #articulo['en_venta'] = elem['on_sale']
                #articulo['solo_online'] = elem['online_only']
                #articulo['ecotax'] = elem['ecotax'] 
                #articulo['cantidad_minima'] = elem['minimal_quantity']
                #articulo['aviso_stock_bajo'] = elem['low_stock_alert']
                articulo['precio'] = elem['price']
                articulo['peso'] = elem['weight']
                #articulo['mostrar_precio'] = elem['show_price']
                #articulo['fecha_alta'] = elem['date_add']
                #articulo['fecha_ultima_modificacion'] = elem['date_upd']
                #articulo['pack_stock_type'] = elem['pack_stock_type']
                articulo['meta_descripcion'] = elem['meta_description']['language']['#text']
                articulo['meta_keywords'] = elem['meta_keywords']['language']['#text']
                articulo['meta_title'] = elem['meta_title']['language']['#text']
                #articulo['link_rewrite'] = elem['link_rewrite']['language']['#text']
                articulo['nombre'] = elem['name']['language']['#text']
                articulo['descripcion'] = elem['description']['language']['#text']
                articulo['descripcion_short'] = elem['description_short']['language']['#text']
                
                #assosiations
                # Guarda los Articulos que tienen EAN, que son los de interés.

                if articulo['ean13']:
                    if len(campos) > 0:
                        articulo_dict = {k:articulo[k] for k in campos if k in articulo}
                        articulos.append(articulo_dict)
                    else:
                        articulos.append(articulo)
            
            except:
                pass
        
        print(articulos)
        return articulos
        
    def get_orders(self, campos=[]):
        #Depende de la API para funcionar, a veces funciona, otras veces dice que no existe, ¿puede ser por tener mas de 4000 pedidos?
        url = "http://lafabricadegolosinas.com/api/orders/?display=full&filter[date_add]=[2021-01-1,2021-5-31]&date=1&output_format=XML&ws_key=K23MFEIG5L7C41U3LNY377JNC9WV1UDE"
        params = {}
        print(url)

        response = requests.get(url, params=params)

        content = response.content
        doc_json_orders = xmltodict.parse(content)

        pedidos = []
        for elem in doc_json_orders["prestashop"]["orders"]["order"]:
            try:
                pedido = {}
                pedido['id_address_delivery'] = elem['id_address_delivery']['#text']
                pedido['id_address_invoice'] = elem['id_address_invoice']['#text']
                pedido['id_cart'] = elem['id_cart']['#text']
                pedido['id_customer'] = elem['id_customer']['#text']
                pedido['current_state'] = elem['current_state']['#text']
                pedido['valid'] = elem['valid']
                pedido['date_add'] = elem['date_add']
                pedido['date_upd'] = elem['date_upd']
                pedido['shipping_number'] = elem['shipping_number']['@notFilterable']
                pedido['total_paid'] = elem['total_paid']
                pedido['reference'] = elem['reference']

                
                

                productos_list = []
                for productos in elem["associations"]["order_rows"]["order_row"]:
                    producto = {}
                    producto["product_name"] = productos["product_name"]
                    producto["product_reference"] = productos["product_reference"]
                    producto["product_price"] = productos["product_price"] 
                
                    productos_list.append(producto)

                pedido['productos'] = productos_list

                '''
                En caso de querer solo los pedidos efectuados, pedidos reales de la empresa.
                '''
                if elem["delivery_number"] == "0":
                    if len(campos) > 0:
                        pedidos_dict = {k: pedido[k] for k in campos if k in pedido}
                        pedidos.append(pedidos_dict)
                    else:
                        pedidos.append(pedido)

                    
               
            except:
                pass
        
        return pedidos

    def get_product_by(self, campo, valor):
        # Supongo que habrá que utilizar filter

        doc_json_by = self.get_filter(option=campo, value=valor)

        productos = self.get_products()

        try:
            for elem in productos:
                if elem[campo] != valor:
                    pass
                else:
                    producto_filter = self.get_producto(json=doc_json_by)
                    return producto_filter
        except:
            pass
            
        print ("El " + str(campo) + " : " + str(valor) + " no corresponde a ningun producto.") 
        
        #return producto
        #pass
    
    def update_producto(self, product_xml, reference):
        '''
            Entrada: referencia a acualizar
                    diccionario con los datos
        '''
        pass

    def add_producto(self, producto):
        url = self.url_base + '/products?display=full&output_format=XML&ws_key=' + self.key + "/post"
        params = {}

        
        xml=open(producto)
        new_product = xmltodict.parse(xml.read())

        print(url)
        print(new_product)

        response = requests.post(url, data=new_product, headers={'Conten-Type': 'text/xml'})
        print(response)

        pass

    def fichero_to_csv(self, fichero, campo="", valor = "" ,  salida='output.xlsx'):
        '''
            Params: fichero de prestashop a exportar
                    fichero excel a convenir
        '''
        #Los Ficheros se tiene que encontrar aqui para poder guardar las funciones y utilizarlas.
        #No se porque, pero si encuentra el fichero, los ejecuta todos, eso crea que de errores.
        FICHEROS = {"Productos" : self.get_products(), "Filter": self.get_product_by(campo=campo, valor=valor), "Pedidos": self.get_orders()}

        if fichero in FICHEROS:
            lista = FICHEROS[fichero]
            df = pd.DataFrame.from_dict(lista)
            df.to_excel(salida)
        else:
            print("Fichero no encontrado")

    def fichero_to_json(self,fichero, campo="", valor = "", json_f="sample.json", campos=[]):
        #FICHEROS = {"Productos" : self.get_products(), "Filter": self.get_product_by(campo=campo, valor=valor), "Pedidos": self.get_orders(), "Prueba": print("Ha fallat")}
        
        FICHEROS = {"Productos" : 1, "Filter": 3, "Pedidos": 2}

        if fichero in FICHEROS:
            if FICHEROS[fichero] == 1:
                 lista = self.get_products(campos=campos)
            elif FICHEROS[fichero] ==2:
                lista = self.get_orders()
                
            with open(json_f, "w") as outfile: 
                json.dump(lista, outfile, separators=(',', ':'))
        else:
            print("Fichero no encontrado")


api = PrestashopApi('http://lafabricadegolosinas.com/api','K23MFEIG5L7C41U3LNY377JNC9WV1UDE')

#print(api.get_product_by_reference(reference="0200394023001"))
#print(api.get_product_by_ean(ean="123456789"))
print(api.add_producto(producto="producto.xml"))

#api.fichero_to_csv(fichero="Filter",campo="reference",valor="21554", salida="producto_especifico.xlsx")
#api.fichero_to_csv(fichero="Pedidos",salida="pedidos.xlsx")

#api.fichero_to_json(fichero="Productos", json_f="productes.json")

#api.fichero_to_json(fichero="Pedidos", json_f="pedidos_filtro.json", campos=['id_address_delivery', 'reference', 'total_paid', 'shipping_number'])




