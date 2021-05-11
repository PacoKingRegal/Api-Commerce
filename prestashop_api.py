import requests
import xmltodict
import pandas as pd

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

    def get_products(self):
        doc_json_products = self.get_data(option="products")

        #print(doc_json)
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
                    articulos.append(articulo)
            
            except:
                pass

        return articulos
        
    def get_orders(self):
        #Depende de la API para funcionar, a veces funciona, otras veces dice que no existe, ¿puede ser por tener mas de 4000 pedidos?
        doc_json_orders = self.get_data(option="orders")

        pedidos = []

        for elem in doc_json_orders["prestashop"]["orders"]["order"]:
            try:
                pedido = {}
                pedido['id'] = elem['id']
                pedido['numero_pedido'] = elem['delivery_number']
                pedido['fecha_pedido'] = elem['date_add']
                pedido['fecha_entrega'] = elem['delivery_date']
                pedido['metodo_pago'] = elem['payment']
                pedido['precio_total_productos'] = elem['total_products_wt']
                pedido['precio_iva'] = elem['total_shipping']
                pedido['precio_total'] = elem['total_paid']
                pedido['reference'] = elem['reference']

                '''
                En caso de querer solo los pedidos efectuados, pedidos reales de la empresa.
                if pedido['numero_pedido']:
                    pedidos.append(pedido)
                '''

                pedidos.append(pedido)
               
            except:
                pass
        return pedidos


    def get_product_by_reference(self, reference):
        # Supongo que habrá que utilizar filter
        doc_json_by_reference = self.get_filter(option="reference", value=reference)

        productos = self.get_products()
        for elem in productos:
            if elem['reference'] != reference:
               pass
            else:
                producto = self.get_producto(json=doc_json_by_reference)
                return producto
        print ("La referencia : " + str(reference) + " no corresponde a ningun producto.")
        
        #return producto
        #pass

    def get_product_by_ean(self, ean):
        # Supongo que habrá que utilizar filter

        doc_json_by_ean = self.get_filter(option="ean13", value=ean)

        productos = self.get_products()
        for elem in productos:
            if elem['ean13'] != ean:
               pass
            else:
                producto_ean = self.get_producto(json=doc_json_by_ean)
                return producto_ean

        print ("El ean13 : " + str(ean) + " no corresponde a ningun producto.")
        

        #return producto
        #pass
    
    def update_producto(self, product_xml, reference):
        '''
            Entrada: referencia a acualizar
                    diccionario con los datos
        '''
        pass

    def add_producto(self, producto):
        url = self.url_base + '/products?display=full&output_format=XML&ws_key=' + self.key + "/put"
        params = {}

        
        xml=open(producto)
        new_product = xmltodict.parse(xml.read())

        print(url)
        print(new_product)

        response = requests.put(url, data=new_product, headers={'Conten-Type':'application/xml'})
        print(response)

        pass

    def fichero_to_csv(self, fichero, valor = "" ,  salida='output.xlsx'):
        '''
            Params: fichero de prestashop a exportar
                    fichero excel a convenir
        '''
        #Los Ficheros se tiene que encontrar aqui para poder guardar las funciones y utilizarlas.
        #No se porque, pero si encuentra el fichero, los ejecuta todos, eso crea que de errores.
        FICHEROS = {"Productos" : self.get_products(), "Pedidos" : self.get_orders(), "Referencia" : self.get_product_by_reference(valor), "EAN" : self.get_product_by_ean(valor)}

        if fichero in FICHEROS:
            lista = FICHEROS[fichero]
            df = pd.DataFrame.from_dict(lista)
            df.to_excel(salida)
        else:
            print("Fichero no encontrado")

        

api = PrestashopApi('http://lafabricadegolosinas.com/api', 'K23MFEIG5L7C41U3LNY377JNC9WV1UDE')

#print(api.get_product_by_reference(reference="0200394023001"))
#print(api.get_product_by_ean(ean="123456789"))
print(api.add_producto(producto="producto.xml"))

#api.fichero_to_csv(fichero="EAN",valor="8412541160525", salida="producto_especifico.xlsx")
#api.fichero_to_csv(fichero="Pedidos", salida="pedidos.xlsx")




