import json
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from function.DynamoManager import DynamoManager
from utils.logger import Logger

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

current_directory = os.path.dirname(os.path.abspath(__file__))
credentials_file_path = os.path.join(current_directory, '..', 'tmp/data', 'credentials.json')


logger = Logger(__name__)


def get_credentials():
    credentials = None

    token_data = DynamoManager.get_gmail_data()

    if token_data:
        if isinstance(token_data['data'], str):
            token = json.loads(token_data['data'])
        credentials = Credentials.from_authorized_user_info(token, SCOPES)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(Request())
            except Exception as e:
                logger.error(f'Error al refrescar las credenciales: {e}')
                DynamoManager.clean_gmail_data()
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file_path, SCOPES)
            credentials = flow.run_local_server(port=0)

        DynamoManager.upload_gmail_data(credentials.to_json())

    return credentials
