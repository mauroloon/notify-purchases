import requests


token = ""


def insert_data_to_notion_table(database_id, data):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2021-08-16",
    }
    payload = {
        "properties": {
            "Nombre": {"title": [{"text": {"content": data["name"]}}]},
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    print(response)
    if response.status_code == 200:
        print("Data inserted successfully!")
    else:
        print("Failed to insert data.")


# Example usage
database_id = ""
data = {"name": "prueba", "amount": 1000, "phone": "+1234567890"}
insert_data_to_notion_table(database_id, data)
