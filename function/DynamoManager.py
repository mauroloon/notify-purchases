import json
from datetime import datetime
from uuid import uuid4

import boto3

REGION_AWS = 'us-east-2'


class DynamoManager:
    @staticmethod
    def upload_gmail_data(data: dict):
        dynamodb = boto3.resource('dynamodb', region_name=REGION_AWS)
        table = dynamodb.Table('Gmails')

        with open('tmp/data/token.json') as token_file:
            token_data = json.load(token_file)

        # Subir el token a DynamoDB
        table.put_item(
            Item={
                'id': str(uuid4()),
                'data': token_data,
                'date': datetime.now().strftime('%Y-%m-%d'),
            }
        )
