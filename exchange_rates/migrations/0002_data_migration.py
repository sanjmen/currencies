from datetime import datetime

from django.db import migrations
from django.conf import settings

from exchange_rates.currencies import CODES


def populate_currencies(apps, schema_editor):
    Currency = apps.get_model("exchange_rates", "Currency")
    for symbol, code, name in CODES:
        Currency.objects.create(symbol=symbol, code=code, name=name)


def populate_exchange_rates(apps, schema_editor):
    Currency = apps.get_model("exchange_rates", "Currency")
    CurrencyExchangeRate = apps.get_model("exchange_rates", "CurrencyExchangeRate")
    currencies = Currency.objects.all()

    source_currency = currencies[0]
    exchanged_currency = currencies[1]
    valuation_date = datetime.now().strftime(settings.DATE_FORMAT)

    CurrencyExchangeRate.objects.create(
        source_currency=source_currency,
        exchanged_currency=exchanged_currency,
        valuation_date=valuation_date,
        rate_value=123.12323,
    )


def populate_providers(apps, schema_editor):
    Provider = apps.get_model("exchange_rates", "Provider")
    Provider.objects.create(
        module_path="exchange_rates.providers.fixer",
        class_name="FixerProvider",
        priority="0",
    )
    Provider.objects.create(
        module_path="exchange_rates.providers.mock",
        class_name="MockProvider",
        priority="3",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("exchange_rates", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(populate_currencies),
        migrations.RunPython(populate_providers),
        migrations.RunPython(populate_exchange_rates),
    ]
