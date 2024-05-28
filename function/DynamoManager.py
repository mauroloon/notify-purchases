import json

import boto3

REGION_AWS = 'us-east-2'


class DynamoManager:
    @staticmethod
    def upload_gmail_data(data: dict):
        dynamodb = boto3.resource('dynamodb', region_name=REGION_AWS)
        table = dynamodb.Table('GmailTokens')

        with open('tmp/data/token.json') as token_file:
            token_data = json.load(token_file)

        # Subir el token a DynamoDB
        table.put_item(
            Item={
                #'User': 'your-user-id',  # Puede ser cualquier identificador único del usuario
                'Data': token_data,
            }
        )
