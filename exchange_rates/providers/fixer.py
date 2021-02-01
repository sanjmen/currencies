import requests

from django.conf import settings

from exchange_rates.providers.base import BaseProvider

BASE_URL = "http://data.fixer.io/api/"


class FixerProvider(BaseProvider):
    def fetch(self, source_currency, exchanged_currency, valuation_date):
        url = BASE_URL + valuation_date
        payload = {
            "access_key": settings.FIXER_API_KEY,
            "base": source_currency.symbol,
            "symbols": exchanged_currency.symbol,
        }

        r = requests.get(url, params=payload)

        if r.status_code == 200:
            data = r.json()
            if data["success"]:
                return data["rates"][str(exchanged_currency)]

        return None
