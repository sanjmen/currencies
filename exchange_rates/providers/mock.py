import random

from exchange_rates.providers.base import BaseProvider


class MockProvider(BaseProvider):
    def fetch(self, source_currency, exchanged_currency, valuation_date):
        return round(random.uniform(1.01, 1.99), 6)