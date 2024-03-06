import hashlib
import json
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Creación del diccionario con los datos del mensaje
# Para mas opciones puede consultar la documentación
# https://api-doc.ccc.uno/?version=latest#e183174f-88eb-448b-be06-e623b928f4ed

data_send = {
    'datetime_from': '2024-01-19 01:00:00',
    'datetime_to': '2024-01-19 23:59:59',
    'page': 1,
    'page_size': 1000,
    'columns': '',
    'options': ['list_columns', 'dispositions', 'call_notes']
    #'passphrase': 'miclave' # en caso de que la campaña se encuentre encriptada se tiene que agregar este campo para poder visualizar los datos correctamente
}

# Endpoint para enviar los datos
url = 'https://api.ccc.uno/ws/CallHistory/Search'

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
