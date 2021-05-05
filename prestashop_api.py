import requests
import xmltodict

import pandas as pd




class PrestashopApi:
    CORRECT_REQUEST = (200, 201)
    FICHEROS = ["Productos", "Pedidos"]
    
    def __init__(self, url_base, key):
        self.url_base = url_base
        self.key = key
        

    def _set_url_request(self, path):
        return self.url_base + '/' + path
    
    def _check_response(self, res):
        if res.status_code not in self.CORRECT_REQUEST:
            print("Error")

    def get_products(self):
        url = self.url_base + '/products?display=full&output_format=XML&ws_key=' + self.key
        params = {}
        print(url)

        response = requests.get(url, params=params)

        content = response.content
        doc_json = xmltodict.parse(content)

        #print(doc_json)
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

        return articulos
        
    def get_orders(self):
        pass

    def get_product_by_reference(self, reference):
        # Supongo que habrá que utilizar filter
        "Oko, solo devolvemos 1"
        pass

    def get_product_by_ean(self, ean):
        # Supongo que habrá que utilizar filter
        "Oko, solo devolvemos 1"
        pass
    
    def update_producto(self, product_xml, reference):
        '''
            Entrada: referencia a acualizar
                    diccionario con los datos
        '''
        pass

    def add_producto(self, producto):
        pass




    def fichero_to_csv(self, fichero, salida='output.xlsx'):
        '''
            Params: fichero de prestashop a exportar
                    fichero excel a convenir
        '''

        if fichero in self.FICHEROS:
            #TODO falta bifurcar 
            lista = self.get_products()
            df = pd.DataFrame.from_dict(lista)
            df.to_excel(salida)
        else:
            print("Ficchero no encontrado")

        




    
api = PrestashopApi('http://lafabricadegolosinas.com/api', 'K23MFEIG5L7C41U3LNY377JNC9WV1UDE')

print(api.get_products())

#api.fichero_to_csv(fichero="Productos", salida="productes.xlsx")
#api.fichero_to_csv(fichero="Pedidos", salida="pedidos.xlsx")




