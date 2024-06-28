from bs4 import BeautifulSoup


def get_payment_data_html(html_string):
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
