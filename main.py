import logging

# from function import DynamoManager
from function import EmailManager
from function import IndicatorManager
from function import NotionManager

logging.getLogger().setLevel(logging.INFO)

if __name__ == '__main__':
    # DynamoManager.upload_gmail_data({})
    email_manager = EmailManager()
    labels = email_manager.get_gmail_payment_label()
    if not labels:
        logging.info('No se ha encontrado la etiqueta de pagos.')
        exit()

    data = email_manager.get_payment_email(labels['id'])

    db_name = 'Saldos mensuales'
    database_id = NotionManager.get_id_data_bases(db_name)
    month_id = NotionManager.get_last_month_id(database_id)
    for d in data:
        print(f"De: {d['from']}")
        print(f"Asunto: {d['subject']}")
        print(f"Monto: {d['monto']}")
        print(f"Fecha: {d['fecha']} {d['hora']}")
        print(f"Comercio: {d['comercio']}")
        print('----------')

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
