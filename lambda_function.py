import logging

from function import EmailManager
from function import NotionManager

# Configura el nivel de logging a INFO
logging.basicConfig(level=logging.INFO)

# Crea un logger
logger = logging.getLogger(__name__)


def lambda_handler(event, context):
    logger.info('Inicio de la función.')
    data = EmailManager.get_payment_email()
    logger.info(f'Datos obtenidos: {data}')
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
            data = {
                'name': d['comercio'],
                'amount': amount,
            }
            result = NotionManager.insert_payment_data_by_month(data, month_id)

        print(result)
