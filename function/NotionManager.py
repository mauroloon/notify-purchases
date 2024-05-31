import json
import os

import requests
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

# Get the token from the environment variables
token = os.getenv('TOKEN_NOTION')
database_id = os.getenv('DATABASE_PAYMENTS')


class NotionManager:
    @staticmethod
    def get_last_month_id(database_id: str) -> str:
        """
        Obtiene el id del mes en la base de datos de Notion.

        Args:
            - database_id (str): Id de la base de datos de Notion.

        """
        url = f'https://api.notion.com/v1/databases/{database_id}/query'

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Notion-Version': '2021-08-16',
        }
        filters = {
            'filter': {'property': 'Nombre', 'text': {'is_not_empty': True}},
            'sorts': [{'property': 'Creacion', 'direction': 'descending'}],
        }

        response = requests.post(url, json=filters, headers=headers)
        data = response.json()
        return data['results'][0]['id']

    @staticmethod
    def get_id_data_bases(db_name: str) -> str:
        """
        Obtiene el id de la base de datos de Notion según el nombre a buscar.

        Args:
            - db_name (str): Nombre de la base de datos a buscar.
        """
        url = 'https://api.notion.com/v1/databases'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Notion-Version': '2021-08-16',
        }
        response = requests.get(url, headers=headers)

        data = json.loads(response.text)
        result_db = ''
        for result in data['results']:
            if 'properties' in result and db_name in result['properties']:
                result_db = result['properties'][db_name]

        return result_db.get('relation', '').get('database_id', '')

    @staticmethod
    def insert_payment_data_by_month(data: dict, month_id: str) -> str:
        """
        Registra un pago en la base de datos de Notion en el mes especificado por el id.

        Args:
            - data (dict): Diccionario con los datos del pago.
                - name (str): Nombre del comercio.
                - amount (int): Monto del pago.
            - month_id (str): Id del mes en la base de datos de Notion.
        """
        url = 'https://api.notion.com/v1/pages'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Notion-Version': '2021-08-16',
        }
        payload = {
            'parent': {'database_id': database_id},
            'properties': {
                'Nombre': {'title': [{'text': {'content': data.get('name')}}]},
                'Monto': {'number': data.get('amount')},
                'Tipo': {'select': {'name': 'Sin categorizar'}},
                'Persona': {'select': {'name': 'Mauricio'}},
                'Saldos mensuales': {'relation': [{'id': month_id}]},
            },
        }
        response = requests.post(url, headers=headers, json=payload)

        return response.text
