import requests
import json
import pandas as pd
from datetime import datetime

# Configuración
# Añadir sus keys desde https://develop.battle.net
client_id = ''
client_secret = ''
region = 'us'  # us, eu, kr, tw, cn (cn es medio raro)
realm_id = '1428' # Quel'Thalas ID

# Obtener token de acceso
def obtener_token(client_id, client_secret):
    url = f'https://{region}.battle.net/oauth/token'
    data = {'grant_type': 'client_credentials'}
    response = requests.post(url, data=data, auth=(client_id, client_secret))
    response.raise_for_status()
    return response.json()['access_token']

# Obtener datos de la subasta de commodities
def obtener_datos_commodities(token):
    url = f'https://{region}.api.blizzard.com/data/wow/auctions/commodities'
    headers = {'Authorization': f'Bearer {token}'}
    params = {'namespace': f'dynamic-{region}', 'locale': 'en_US'}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

# Guardar datos en un archivo Excel
def guardar_datos_en_excel(datos, file_path):
    df = pd.DataFrame(datos)
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    df['date'] = fecha_actual
    df.to_excel(file_path, index=False)

# main
if __name__ == '__main__':
    token = obtener_token(client_id, client_secret)
    ## Obtener datos de commodities y procesarlos
    datos_commodities = obtener_datos_commodities(token)
    print(datos_commodities)

    all_items = []

    # Iterar sobre los commodities
    for commodity in datos_commodities['auctions']:
        item_id = commodity['item']['id']
        unit_price = commodity['unit_price'] / 10000  # Se divide en 10000 dado a que retorna el precio en cobre
        quantity = commodity['quantity']

        # Agregar el objeto a la lista
        all_items.append({
            'item_id': item_id,
            'unit_price': unit_price,
            'quantity': quantity,
        })

    # Convertir la lista de objetos a un DataFrame de pandas
    df = pd.DataFrame(all_items)

    # Guardar los datos en un archivo Excel
    current_date = datetime.now().strftime('%Y-%m-%d')
    df.to_excel(f'commodities_snapshot-{current_date}.xlsx', index=False)

    print(f"Datos almacenados correctamente en 'commodities_snapshot-{current_date}.xlsx'")
