## README API


### Archivos
#### Datos subasta
Los archivos con datos de la subasta se guardan actualmente con el formato: 'commoditiers-snapshot-{fecha:año-mes-dia}.xslx'.

Esta posee 3 columnas, 'item_id' que es el identificador, 'unit_price' que es el precio en oro y 'quantity' que corresponde a la cantidad para ese item_id y unit_price (pueden haber distintos precios para un mismo item_id, y por ende distintas cantidades).

#### Nombres objetos
Los nombres de los objetos estan guardados en 'item_cache.xslx', con una columna asociada al id y otra al nombre, actualmente no estan separados los objetos que tienen distintos rangos (gracias api de blizzard)

### Programas
Para correr los programas se necesita agregar sus llaves privadas, que se pueden obtener en https://develop.battle.net
#### ah_commodities_parser.py
Obtiene un snapshot de las commodities de la subasta y lo guarda con el formato: 'commoditiers-snapshot-{fecha:año-mes-dia}.xslx'

#### name_parser.py
Obtiene los nombres de los objetos de un snapshot y los guarda en 'item_cache.xslx'