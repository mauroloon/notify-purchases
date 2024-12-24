import os
from datetime import datetime
from uuid import uuid4

import boto3
from dotenv import load_dotenv

load_dotenv()


REGION_AWS = os.getenv('REGION')


class DynamoManager:
    @staticmethod
    def upload_gmail_data(data: dict) -> None:
        """
        Sube el token a DynamoDB.

        Args:
            - data (dict): Token de Gmail.

        Returns:
            - None
        """
        dynamodb = boto3.resource('dynamodb', region_name=REGION_AWS)
        table = dynamodb.Table('Gmails')

        # Subir el token a DynamoDB
        table.put_item(
            Item={
                'id': str(uuid4()),
                'data': data,
                'date': datetime.now().strftime('%Y-%m-%d'),
            }
        )

    @staticmethod
    def get_gmail_data() -> dict:
        """
        Obtiene el último item de la tabla Gmails.

        Returns:
            - dict: Último item de la tabla Gmails.
        """
        dynamodb = boto3.resource('dynamodb', region_name=REGION_AWS)
        table = dynamodb.Table('Gmails')

        response = table.scan()
        items = response['Items']
        last_item = items[-1] if items else None
        return last_item

    @staticmethod
    def clean_gmail_data() -> None:
        """
        Limpia la tabla Gmails.

        Returns:
            - None
        """
        dynamodb = boto3.resource('dynamodb', region_name=REGION_AWS)
        table = dynamodb.Table('Gmails')

        response = table.scan()
        items = response['Items']
        for item in items:
            table.delete_item(Key={'id': item['id']})
        return
