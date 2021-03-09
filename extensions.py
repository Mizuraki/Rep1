import requests
import json
from config import keys


class ConvertionExteprion(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionExteprion(f'Не возможно перевести одинаковые валюту {base}.')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionExteprion(f'Не удалось обработать валюту {quote}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionExteprion(f'Не удалось обработать валюту {base}.')

        try:
            for i in range(len(amount)):
                amount = amount.replace(',', '.')
            amount = float(amount)
        except ValueError:
            raise ConvertionExteprion(f'Не удалось обработать количество {quote}.')

        r = requests.get(f'https://api.exchangeratesapi.io/latest?base={quote_ticker}&symbols={base_ticker}')
        total = json.loads(r.content)["rates"][keys[base]]
        total_base = round(total*amount, 2)
        return total_base