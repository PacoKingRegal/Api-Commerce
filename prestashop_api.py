import requests
import xmltodict
import pandas as pd

class PrestashopApi:
    CORRECT_REQUEST = (200, 201)
        
    def __init__(self, url_base, key):
        self.url_base = url_base
        self.key = key
        
    def get_producto(self, json):
        for elem in json ["prestashop"]["products"]["product"]:
            try:  
                #Se han comentado los campos que no se necesitan.  
                articulo = {}
    
                articulo['id_articulo'] = elem['id']
                articulo['rererence'] = elem['reference']
                articulo['id_categoria'] = elem['id_category_default']['@xlink:href']
                articulo['ean13'] = elem['ean13']
                articulo['precio'] = elem['price']
                articulo['peso'] = elem['weight']
                articulo['meta_descripcion'] = elem['meta_description']['language']['#text']
                articulo['meta_keywords'] = elem['meta_keywords']['language']['#text']
                articulo['meta_title'] = elem['meta_title']['language']['#text']
                articulo['nombre'] = elem['name']['language']['#text']
                articulo['descripcion'] = elem['description']['language']['#text']
                articulo['descripcion_short'] = elem['description_short']['language']['#text']
                
                #assosiations
                # Guarda los Articulos que tienen EAN, que son los de interés.
                print(articulo)
                
            except:
                pass

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
    
                articulo['id_articulo'] = elem['id']
                articulo['rererence'] = elem['reference']
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
        #doc_json_orders = self.get_data(option="order")

        #print(doc_json_orders)
        pass

    def get_product_by_reference(self, reference):
        # Supongo que habrá que utilizar filter
        doc_json_by_reference = self.get_filter(option="reference", value=reference)

        producto = self.get_producto(json=doc_json_by_reference)

        df = pd.DataFrame.from_dict(doc_json_by_reference)
        df.to_excel("producto_especifico.xlsx")
        
        #pass

    def get_product_by_ean(self, ean):
        # Supongo que habrá que utilizar filter
        doc_json_by_ean = self.get_filter(option="ean13", value=ean)

        producto = self.get_producto(json=doc_json_by_ean)

        df = pd.DataFrame.from_dict(doc_json_by_ean)
        df.to_excel("producto_especifico.xlsx")

        pass
    
    def update_producto(self, product_xml, reference):
        '''
            Entrada: referencia a acualizar
                    diccionario con los datos
        '''
        pass

    def add_producto(self, producto):
        pass

    def fichero_to_csv(self, fichero, referencia = "" ,  salida='output.xlsx'):
        '''
            Params: fichero de prestashop a exportar
                    fichero excel a convenir
        '''
        #Los Ficheros se tiene que encontrar aqui para poder guardar las funciones y utilizarlas.
        FICHEROS = {"Productos" : self.get_products(), "Pedidos" : self.get_orders(), "Referencia" : self.get_product_by_reference(referencia)}

        if fichero in FICHEROS:
            lista = FICHEROS[fichero]
            df = pd.DataFrame.from_dict(lista)
            df.to_excel(salida)
        else:
            print("Ficchero no encontrado")

        

api = PrestashopApi('http://lafabricadegolosinas.com/api', 'K23MFEIG5L7C41U3LNY377JNC9WV1UDE')

#print(api.get_product_by_ean(reference="9318590025002"))
#print(api.get_product_by_ean(ean="8437006219600"))

#api.fichero_to_csv(fichero="Productos", salida="productes.xlsx")
#api.fichero_to_csv(fichero="Pedidos", salida="pedidos.xlsx")




