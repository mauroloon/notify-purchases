from function import EmailManager
from function import NotionManager

if __name__ == '__main__':
    data = EmailManager.get_payment_email()

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
