import requests
import os
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

# Get the token from the environment variables
token = os.getenv("TOKEN_NOTION")
database_id = os.getenv("DATABASE_PAYMENTS")
# TODO ver como obtener el mes actual
month_id = os.getenv("MONTH_ID")


class NotionManager:
    @staticmethod
    def insert_data_to_notion_table(data: dict):
        url = "https://api.notion.com/v1/pages"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": "2021-08-16",
        }
        payload = {
            "parent": {"database_id": database_id},
            "properties": {
                "Nombre": {"title": [{"text": {"content": data.get("name")}}]},
                "Monto": {"number": data.get("amount")},
                "Tipo": {"select": {"name": "Sin categorizar"}},
                "Persona": {"select": {"name": "Mauricio"}},
                "Saldos mensuales": {"relation": [{"id": month_id}]},
            },
        }
        response = requests.post(url, headers=headers, json=payload)

        return response.text
