import logging

from function import EmailManager
from function import IndicatorManager
from function import NotionManager

logging.getLogger().setLevel(logging.INFO)


def lambda_handler(event, context):
    logging.info('Inicio de la función.')
    email_manager = EmailManager()
    labels = email_manager.get_gmail_payment_label()
    if not labels:
        return {
            'statusCode': 200,
            'body': {
                'message': 'No se ha encontrado la etiqueta de pagos.',
            },
        }

    data = email_manager.get_payment_email(labels)

    db_name = 'Saldos mensuales'
    database_id = NotionManager.get_id_data_bases(db_name)
    month_id = NotionManager.get_last_month_id(database_id)

    if not data:
        return {
            'statusCode': 200,
            'body': {
                'message': 'No hay correos.',
            },
        }

    for d in data:
        logging.info(
            'Pago',
            {
                'from': d['from'],
                'subject': d['subject'],
                'monto': d['monto'],
                'fecha': d['fecha'],
                'hora': d['hora'],
                'comercio': d['comercio'],
            },
        )

        if 'USD' not in d['monto']:
            amount = int(d['monto'].replace('$', '').replace('.', '').replace(',', '.'))
        else:
            value_usd = IndicatorManager.get_value_by_code('dolar')
            amount = int(
                float(d['monto'].replace('USD', '').replace(' ', '').replace(',', '.')) * value_usd
            )

        data = {
            'name': d['comercio'],
            'amount': amount,
        }
        NotionManager.insert_payment_data_by_month(data, month_id)

        logging.info(
            'Se ha insertado el pago de '
            + d['monto']
            + ' en '
            + d['comercio']
            + ' en la base de datos.'
        )

    return {
        'statusCode': 200,
        'body': {
            'message': 'Se han insertado los pagos en la base de datos.',
        },
    }
