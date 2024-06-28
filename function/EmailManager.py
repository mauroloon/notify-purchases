import base64
from datetime import datetime
from datetime import timedelta

# from googleapiclient.discovery import build
from google_auth import make_build

from utils import Logger
from utils import get_credentials
from utils import get_payment_data_html

logger = Logger(__name__)


class EmailManager:
    def __init__(self) -> None:
        self.credentials = get_credentials()
        self.service = make_build('gmail', 'v1', credentials=self.credentials)

    def check_credentials(self) -> bool:
        """
        Verifica si las credenciales son válidas.

        Returns:
            - bool: True si las credenciales son válidas, False en caso contrario.
        """
        if not self.credentials:
            logger.info('No hay credenciales.')
            return False
        return True

    def get_gmail_payment_label(self) -> dict:
        """
        Obtiene la etiqueta de pagos registrados.

        Returns:
            - dict: Etiqueta de pagos registrados.
        """
        if not self.check_credentials:
            return

        results = self.service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No hay etiquetas.')
            return
        payment_label = next(
            (label for label in labels if label['name'] == 'Pagos registrados'), None
        )
        return payment_label

    def add_label_to_email(self, message_id: str, label_id: str) -> None:
        """
        Agrega una etiqueta a un correo.

        Args:
            - message_id (str): ID del mensaje.
            - label_id (str): ID de la etiqueta.

        Returns:
            - None
        """
        if not self.check_credentials:
            return

        self.service.users().messages().modify(
            userId='me', id=message_id, body={'addLabelIds': [label_id]}
        ).execute()

    def get_payment_email(self, label: dict = None) -> list:
        """
        Obtiene los correos de pagos realizados.

        Args:
            - label (str): ID de la etiqueta.

        Returns:
            - list: Lista de pagos realizados.

        """
        if not self.check_credentials:
            return

        label_id = label['id']
        label_name = label['name']
        date_now = (datetime.now() - timedelta(days=1)).strftime('%Y/%m/%d')
        # date_now = '2024/04/18' # Test
        result = (
            self.service.users()
            .messages()
            .list(userId='me', q=f'after:{date_now} from:contacto@bci.cl -label:{label_name}')
            .execute()
        )
        messages = result.get('messages', [])
        data = []

        if not messages:
            print('No hay mensajes.')
            return

        # TODO: optimizar
        for message in messages:
            msg = self.service.users().messages().get(userId='me', id=message['id']).execute()
            # Decodificar el mensaje
            message_data = msg['payload']['headers']
            for values in message_data:
                name = values['name']
                if name == 'From':
                    from_address = values['value']
                if name == 'Subject':
                    subject = values['value']

            if subject == 'Notificación de uso de tu tarjeta de crédito':
                message_body = base64.urlsafe_b64decode(
                    msg['payload']['body']['data'].encode('UTF-8')
                ).decode('UTF-8')
                monto, fecha, comercio, hora = get_payment_data_html(message_body)
                data.append(
                    {
                        'from': from_address,
                        'subject': subject,
                        'monto': monto,
                        'fecha': fecha,
                        'comercio': ' '.join(comercio.title().split()),
                        'hora': hora,
                    }
                )
                self.add_label_to_email(message['id'], label_id)

        return data
