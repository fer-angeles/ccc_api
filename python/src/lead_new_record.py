import hashlib
import json
import requests
import os
import time
import sys
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()

# Creación del diccionario con los datos del mensaje
# En el caso de agregar un nuevo Lead debe conicidir el nombre y el número de columnas de la lista con la que se creo la campaña
# En el arreglo de lead se puede enviar
data_send = {
     'campaign_id': '123456',
     'Leads': [
          {
               'TEL': '8112345678',
               'GRUPO': 'Cel',
               'US': '42488',
               'CK': '2',
               'NOM': 'Víctor Reyes',
               'SMS': 'HOLA, Gracias.',
               'BRAND': 'Palacio de Hierro',
               'BALANCE': '5000',
               'DATE': '2024-02-25',
               'PRODUCT': 'Tarjeta Black',
               'URL': 'https//www.youtube.com/',
               'US2': 'GSDaniel',
               'US3': 'QAAdmin',
               'US4': 'Agente007'
        }
    ]
}

# Endpoint para enviar los datos
url = 'https://api.ccc.uno/ws/Lead'

# Usuario proporcionado por soporte
user = os.getenv('API_CCC_USER')

# ID de cliente proporcionado por soporte
client_id = os.getenv('API_CCC_CLIENT_ID')

# Contraseña  - proporcionado por soporte
secret = os.getenv('API_CCC_SECRET')

# Contraseña encriptada en sha256
secret_hash = hashlib.sha256(secret.encode()).hexdigest()

# Conversión de los datos a formato JSON para el procesamiento por la API
data_send_json = json.dumps(data_send, separators=(',', ':'))

# Fecha y hora de la petición
request_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Creación de token1 usando sha256 del string del JSON
token1 = hashlib.sha256(data_send_json.encode()).hexdigest()

# Creación de token2 mediante concatenación de client_id, user, secret_hash
token2 = hashlib.sha256(f"{client_id}:{user}:{secret_hash}".encode()).hexdigest()

# Token final mediante concatenación de token1, token2 y request_date_time
auth_token = hashlib.sha256(f"{token1}:{token2}:{request_date_time}".encode()).hexdigest()

# Campos para la solicitud
fields = f"AuthUsername = {user}\nAuthToken = {auth_token}\nRequestDateTime = {request_date_time}\nData = {data_send_json}"

# Configuración para el uso de requests en Python
headers = {'Content-Type': 'text/plain'}
response = requests.post(url, headers=headers, data=fields, verify=True)

# Imprimir respuesta
json_str = json.dumps(response.json(), indent=4)
print(json_str)