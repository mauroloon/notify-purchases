import logging


class Logger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def debug(self, message: str) -> None:
        """
        Registra un mensaje de depuración.

        Args:
            - message: str
                Mensaje de depuración.

        Authors:
            - Mauricio Quezada

        Created:
            - 06/06/2024
        """
        self.logger.debug(message)

    def info(self, message: str) -> None:
        """
        Registra un mensaje de información.

        Args:
            - message: str
                Mensaje de información.

        Authors:
            - Mauricio Quezada

        Created:
            - 06/06/2024
        """
        self.logger.info(message)

    def warning(self, message):
        """
        Registra un mensaje de advertencia.

        Args:
            - message: str
                Mensaje de advertencia.

        Authors:
            - Mauricio Quezada

        Created:
            - 06/06/2024
        """
        self.logger.warning(message)

    def error(self, message):
        """
        Registra un mensaje de error.

        Args:
            - message: str
                Mensaje de error.

        Authors:
            - Mauricio Quezada

        Created:
            - 06/06/2024
        """
        self.logger.error(message)

    def critical(self, message):
        """
        Registra un mensaje crítico.

        Args:
            - message: str
                Mensaje crítico.

        Authors:
            - Mauricio Quezada

        Created:
            - 06/06/2024
        """
        self.logger.critical(message)
