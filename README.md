
# Notificador de pago

Proyecto personalizado para el registro de pagos en notion a través de la lectura de correos de pagos.




## Installation

Instalar con python 3.11.8

```bash
  pip install -r requirements.txt
```

Configurar Aws Cli 2

```
  aws configure
```

Crear tabla 'Gmails' en Dyanmo DB
## Optimizations

- Duración del token de gmail (al ser una aplicación test, solamente dura 7 días).



## Environment Variables

Para correr el proyecto se necesitan las siguientes variables de entorno.

`TOKEN_NOTION`: Identificación de Notion.

`DATABASE_PAYMENTS`: Identificador de la db de notion, donde se registran los pagos.

`REGION`: Región de Aws, donde se almacenan los datos de DynamoDB.

## Authors

- [@Mauroloon](https://github.com/mauroloon)
