from datetime import datetime

from django.conf import settings

from exchange_rates.models import Currency, Provider


def get_exchange_rate_data(
    source_currency, exchanged_currency, valuation_date, provider
):
    if not isinstance(provider, Provider):
        try:
            provider = Provider.objects.get(class_name=provider)
        except Provider.DoesNotExist as e:
            raise Exception(e)

    if not isinstance(source_currency, Currency):
        try:
            source_currency = Currency.objects.get(symbol=source_currency.upper())
        except Currency.DoesNotExist as e:
            raise Exception(e)

    if not isinstance(exchanged_currency, Currency):
        try:
            exchanged_currency = Currency.objects.get(symbol=exchanged_currency.upper())
        except Currency.DoesNotExist as e:
            raise Exception(e)

    if not isinstance(valuation_date, datetime):
        try:
            valuation_date = datetime.fromisoformat(valuation_date)
        except ValueError as e:
            raise Exception(e)

    valuation_date = valuation_date.strftime(settings.DATE_FORMAT)
    adapter = provider.get_adapter()

    return adapter.fetch(source_currency, exchanged_currency, valuation_date)
