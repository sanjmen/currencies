class BaseProvider(object):
    """Base class for currency rates data providers"""

    def fetch(self, source_currency, exchanged_currency, valuation_date):
        """Subclasses must implement this to provide currency exchange rates"""
        raise NotImplementedError()