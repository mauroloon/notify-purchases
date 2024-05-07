from function import EmailManager
from function import NotionManager

if __name__ == '__main__':
    data = EmailManager.get_payment_email()
    for d in data:
        print(f"De: {d['from']}")
        print(f"Asunto: {d['subject']}")
        print(f"Monto: {d['monto']}")
        print(f"Fecha: {d['fecha']} {d['hora']}")
        print(f"Comercio: {d['comercio']}")
        print('----------')

        amount = int(d['monto'].replace('$', '').replace('.', '').replace(',', '.'))
        data = {
            'name': d['comercio'],
            'amount': amount,
        }
        result = NotionManager.insert_data_to_notion_table(data)

        print(result)
