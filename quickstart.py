import os.path
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def main():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    """ results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])

    if not labels:
      print("No labels found.")
      return
    print("Labels:")
    for label in labels:
      print(label["name"]) """

    result = service.users().messages().list(userId='me').execute()
    messages = result.get('messages', [])

    if not messages:
        print("No hay mensajes.")
    else:
        print("Mensajes:")
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            # Decodificar el mensaje
            message_data = msg['payload']['headers']
            for values in message_data:
                name = values['name']
                if name == 'From':
                    from_address = values['value']
                if name == 'Subject':
                    subject = values['value']
            
            if subject == 'Notificación de uso de tu tarjeta de crédito':   
                
                message_body = base64.urlsafe_b64decode(msg['payload']['body']['data'].encode("UTF-8")).decode("UTF-8")
                monto, fecha, comercio, hora = extraer_informacion(message_body)
                print(f"De: {from_address}")
                print(f"Asunto: {subject}")
                print(f"Monto: {monto}")
                print(f"Fecha: {fecha} {hora}")
                print(f"Comercio: {comercio}")
                print("----------")

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")

from bs4 import BeautifulSoup

def extraer_informacion(html_string):
    # Crear un objeto BeautifulSoup
    soup = BeautifulSoup(html_string, 'html.parser')

    # Encontrar la fila que contiene la información del monto, la fecha y el comercio
    fila_info = soup.find('tr', {'style': 'background-color: #ebebec;'})

    # Extraer el monto
    monto = fila_info.find_all('td')[1].get_text(strip=True)

    # Encontrar la fila que contiene la fecha
    fila_fecha = fila_info.find_next_sibling('tr')

    # Extraer la fecha
    fecha = fila_fecha.find_all('td')[1].get_text(strip=True)

    # Encontrar la fila que contiene el comercio
    fila_hora = fila_fecha.find_next_sibling('tr')

    # Extraer el comercio
    hora = fila_hora.find_all('td')[1].get_text(strip=True)
    
    fila_comercio = fila_hora.find_next_sibling('tr')

    # Extraer el comercio
    comercio = fila_comercio.find_all('td')[1].get_text(strip=True)

    return monto, fecha, comercio, hora


if __name__ == "__main__":
  main()