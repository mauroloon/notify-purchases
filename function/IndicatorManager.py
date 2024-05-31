import requests


class IndicatorManager:
    @staticmethod
    def get_value_by_code(code: str) -> int:
        """
        Get the value of the indicator by code.

        Args:
            - code: str
                code of the indicator.

        Returns:
            - int
                Round value of the indicator.
        """
        endpoint = 'https://mindicador.cl/api'
        response = requests.get(endpoint)
        data = response.json()
        return int(data.get(code, {}).get('valor', 0))
