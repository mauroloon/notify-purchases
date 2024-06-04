import json
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from function.DynamoManager import DynamoManager

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


# Obtener la ruta absoluta del directorio actual
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construir las rutas a los archivos credentials.json y token.json
credentials_file_path = os.path.join(current_directory, '..', 'tmp/data', 'credentials.json')
token_file_path = os.path.join(current_directory, '..', 'tmp/data', 'token.json')


def get_credentials():
    credentials = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    token_data = DynamoManager.get_gmail_data()

    if token_data:
        if isinstance(token_data['data'], str):
            token = json.loads(token_data['data'])
        credentials = Credentials.from_authorized_user_info(token, SCOPES)

    """ if os.path.exists(token_file_path):
        credentials = Credentials.from_authorized_user_file(token_file_path, SCOPES) """

    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file_path, SCOPES)
            credentials = flow.run_local_server(port=0)
        """ # Save the credentials for the next run
        with open(token_file_path, 'w') as token:
            token.write(credentials.to_json()) """

        DynamoManager.upload_gmail_data(credentials.to_json())

    return credentials
