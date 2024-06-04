import requests
import pandas as pd
import time
import os
from requests.exceptions import HTTPError

# Configuración
# Añadir sus keys desde https://develop.battle.net
client_id = ''
client_secret = ''
region = 'us'  # us, eu, kr, tw, cn (cn es medio raro)
locale = 'es_MX'  # Latin American Spanish

# Obtener token de acceso
def obtener_token(client_id, client_secret):
    url = f'https://{region}.battle.net/oauth/token'
    data = {'grant_type': 'client_credentials'}
    response = requests.post(url, data=data, auth=(client_id, client_secret))
    response.raise_for_status()
    return response.json()['access_token']

# Obtener detalles del item por item_id
def obtener_nombre_item(token, item_id, retries=3, backoff_factor=0.3):
    """Reintentar la solicitud"""
    for n in range(retries):
        try:
            response = requests.get(
                f'https://us.api.blizzard.com/data/wow/item/{item_id}?namespace=static-us&locale=es_MX',
                headers={'Authorization': f'Bearer {token}'}
            )
            response.raise_for_status()
            item_name = response.json()['name']
            item_cache[item_id] = item_name  # Actualizar el item_cache
            guardar_item_cache(item_cache, 'item_cache.xlsx')  # Guardar
            return item_name
        except HTTPError as e:
            if e.response.status_code >= 500:
                print(f'Retry #{n}: Server error: {e}, retrying in {backoff_factor * (2 ** n)} seconds...')
                time.sleep(backoff_factor * (2 ** n))
            else:
                raise
    raise Exception('Server error, all retries failed.')

# Guardar item cache en archivo Excel
def guardar_item_cache(item_cache, file_path):
    df = pd.DataFrame(list(item_cache.items()), columns=['item_id', 'item_name'])
    df.to_excel(file_path, index=False)

# Cargar item cache de archivo Excel (si existe)
def cargar_item_cache(file_path):
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        return dict(zip(df['item_id'], df['item_name']))
    return {}

# main
if __name__ == '__main__':
    token = obtener_token(client_id, client_secret)

    # Leer item_ids desde un archivo
    item_ids = []
    with open('items.txt', 'r') as file:
        for line in file:
            item_id = int(line.strip())
            item_ids.append(item_id)

    item_cache = cargar_item_cache('item_cache.xlsx')

    for item_id in item_ids:
        if item_id not in item_cache:
            item_cache[item_id] = obtener_nombre_item(token, item_id)
            # Evitar el limit rate
            time.sleep(0.05)
            print(f'Added item: {item_id} - {item_cache[item_id]}')

    guardar_item_cache(item_cache, 'item_cache.xlsx')
    print("Item cache almacenado correctamente en 'item_cache.xlsx'")