import requests
import json
import pandas as pd
from datetime import datetime

# Configuración
client_id = ""
client_secret = ""

region = 'us'  # Cambia al region que corresponda: us, eu, kr, tw, cn
realm_id = '1428'  # Quel'Thalas ID

# Obtener token de acceso
def obtener_token(client_id, client_secret):
    url = f'https://{region}.battle.net/oauth/token'
    data = {'grant_type': 'client_credentials'}
    response = requests.post(url, data=data, auth=(client_id, client_secret))
    response.raise_for_status()
    return response.json()['access_token']

# Obtener datos de la casa de subastas
def obtener_datos_subasta(token, realm_id):
    url = f'https://{region}.api.blizzard.com/data/wow/connected-realm/{realm_id}/auctions'
    headers = {'Authorization': f'Bearer {token}'}
    params = {'namespace': f'dynamic-{region}', 'locale': 'es_MX'}  # Asegúrate de usar el locale correcto
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

# Leer item_ids desde un archivo
def leer_item_ids(file_path):
    items = {}
    with open(file_path, 'r') as file:
        for line in file:
            item_id, item_name = line.strip().split(', ')
            items[int(item_id)] = item_name
    return items

# Filtrar datos de subasta por item_ids
def filtrar_datos_por_item_ids(datos_subasta, items):
    items_filtrados = []
    for subasta in datos_subasta['auctions']:
        item_id = subasta['item']['id']
        if item_id in items:
            # Debug: Imprimir subasta para verificar detalles
            print(f"Subasta encontrada para el ítem {items[item_id]} (ID: {item_id})")
            items_filtrados.append({
                'item_id': item_id,
                'item_name': items[item_id],
                'quantity': subasta['quantity'],
                'unit_price': subasta.get('unit_price', subasta.get('buyout', 0)) / 10000,  # Dividir para convertir de cobre a oro
                'time_left': subasta['time_left']
            })
    return items_filtrados

# Guardar datos en un archivo Excel
def guardar_datos_en_excel(datos, file_path):
    df = pd.DataFrame(datos)
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    df['date'] = fecha_actual
    df.to_excel(file_path, index=False)

# Programa principal
if __name__ == '__main__':
    token = obtener_token(client_id, client_secret)
    datos_subasta = obtener_datos_subasta(token, realm_id)
    
    # Debug: Imprimir algunos datos de la subasta para ver qué se está recibiendo
    print("Número total de subastas recibidas:", len(datos_subasta['auctions']))
    if datos_subasta['auctions']:
        for auction in datos_subasta['auctions'][:5]:  # Imprimir las primeras 5 subastas para verificar
            print(json.dumps(auction, indent=4, ensure_ascii=False))

    items = leer_item_ids('items.txt')
    print("Items a buscar:", items)  # Verificar que se están leyendo los ítems correctamente

    datos_filtrados = filtrar_datos_por_item_ids(datos_subasta, items)
    
    if datos_filtrados:
        guardar_datos_en_excel(datos_filtrados, 'subasta_datos.xlsx')
        print('Datos de la subasta guardados en subasta_datos.xlsx')
    else:
        print('No se encontraron subastas para los item_ids proporcionados.')
