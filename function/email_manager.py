import base64

from googleapiclient.discovery import build

from utils import get_credentials
from utils import get_payment_data_html
from datetime import datetime


class EmailManager:
    @staticmethod
    def get_payment_email() -> list:
        creds = get_credentials()
        if not creds:
            print("No hay credenciales.")
            return
        service = build("gmail", "v1", credentials=creds)
        date_now = datetime.now().strftime("%Y/%m/%d")
        # date_now = '2024/04/18' # Test
        result = (
            service.users()
            .messages()
            .list(userId="me", q=f"after:{date_now} from:contacto@bci.cl")
            .execute()
        )
        messages = result.get("messages", [])
        data = []

        if not messages:
            print("No hay mensajes.")
            return

        # TODO: optimizar
        for message in messages:
            msg = (
                service.users().messages().get(userId="me", id=message["id"]).execute()
            )
            # Decodificar el mensaje
            message_data = msg["payload"]["headers"]
            for values in message_data:
                name = values["name"]
                if name == "From":
                    from_address = values["value"]
                if name == "Subject":
                    subject = values["value"]

            if subject == "Notificación de uso de tu tarjeta de crédito":

                message_body = base64.urlsafe_b64decode(
                    msg["payload"]["body"]["data"].encode("UTF-8")
                ).decode("UTF-8")
                monto, fecha, comercio, hora = get_payment_data_html(message_body)
                data.append(
                    {
                        "from": from_address,
                        "subject": subject,
                        "monto": monto,
                        "fecha": fecha,
                        "comercio": comercio,
                        "hora": hora,
                    }
                )

        return data