import logging

logging.getLogger().setLevel(logging.INFO)


def lambda_handler(event, context):
    logging.info('Inicio de la función.')

    return {
        'statusCode': 200,
        'body': {
            'message': 'Se han insertado los pagos en la base de datos.',
        },
    }
