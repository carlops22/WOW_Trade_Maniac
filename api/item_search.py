import json
import requests

# Configuración
client_id = ''
client_secret = ''
region = 'us'  # Cambia al region que corresponda: us, eu, kr, tw, cn
locale = 'es_MX'  # Cambia al locale que corresponda

# Obtener token de acceso
def obtener_token(client_id, client_secret):
    url = f'https://{region}.battle.net/oauth/token'
    data = {'grant_type': 'client_credentials'}
    response = requests.post(url, data=data, auth=(client_id, client_secret))
    response.raise_for_status()
    return response.json()['access_token']

# Obtener información del ítem
def obtener_informacion_item(token, item_id):
    url = f'https://{region}.api.blizzard.com/data/wow/item/{item_id}'
    headers = {'Authorization': f'Bearer {token}'}
    params = {'namespace': f'static-{region}', 'locale': locale}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

# Leer item_ids desde un archivo
def leer_item_ids(file_path):
    item_ids = []
    with open(file_path, 'r') as file:
        for line in file:
            item_id, item_name = line.strip().split(', ')
            item_ids.append((int(item_id), item_name))
    return item_ids

# Programa principal
if __name__ == '__main__':
    token = obtener_token(client_id, client_secret)
    item_ids = leer_item_ids('items.txt')

    for item_id, item_name in item_ids:
        try:
            item_info = obtener_informacion_item(token, item_id)
            print(f"Información del ítem '{item_name}' (ID: {item_id}):")
            print(json.dumps(item_info, indent=4, ensure_ascii=False))
        except requests.exceptions.HTTPError as err:
            print(f"Error al obtener información del ítem '{item_name}' (ID: {item_id}): {err}")
