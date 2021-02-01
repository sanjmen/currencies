from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from exchange_rates.data import get_exchange_rate_data
from exchange_rates.models import Currency, Provider, CurrencyExchangeRate


class Command(BaseCommand):
    help = """
        Run exchange rates data retrieval procedure.
        $ python manage.py update_exchange_rate eur/usd --date 2021-02-01 --provider MockProvider
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "currency_pair",
            type=str,
            help="Currency pair to fetch exchange rates. Pair in format <base>/<quote> (EUR/USD, USD/CHF)",
        )

        parser.add_argument(
            "--date",
            dest="date",
            help="Valuation date to update exchange rates. Date in format YYYY-MM-DD",
        )

        parser.add_argument(
            "--provider",
            dest="provider",
            help="Provider class name to update exchange rates from. i.e: MockProvider.",
        )

    def handle(self, *args, **options):
        currency_pair = options["currency_pair"]
        if currency_pair.find("/") == -1:
            raise CommandError("Pair must be in format <base>/<quote>, like EUR/USD")

        currency_pair = currency_pair.upper().split("/")

        try:
            source_currency = Currency.objects.get(symbol=currency_pair[0])
            exchanged_currency = Currency.objects.get(symbol=currency_pair[1])
        except Currency.DoesNotExist as e:
            raise CommandError(e)

        if options["date"]:
            valuation_date = options["date"]
            try:
                valuation_date = datetime.fromisoformat(valuation_date)
            except ValueError as e:
                raise CommandError(e)
        else:
            valuation_date = datetime.now()

        valuation_date = valuation_date.strftime(settings.DATE_FORMAT)

        try:
            exchange_rate = CurrencyExchangeRate.objects.filter(
                source_currency=source_currency,
                exchanged_currency=exchanged_currency,
                valuation_date=valuation_date,
            )
            if exchange_rate:
                self.stdout.write(
                    self.style.SUCCESS(
                        "Exchange Rate for {}/{} pair with date:{} already exists.".format(
                            source_currency,
                            exchanged_currency,
                            valuation_date,
                        )
                    )
                )
                exit(0)
        except Exception as e:
            raise CommandError(e)

        if options["provider"]:
            provider = options["provider"]
            try:
                provider = Provider.objects.get(class_name=provider)
            except Provider.DoesNotExist as e:
                raise CommandError(e)
        else:
            provider = Provider.objects.default().first()

        try:
            rate_value = get_exchange_rate_data(
                source_currency, exchanged_currency, valuation_date, provider
            )

            exchange_rate = CurrencyExchangeRate.objects.create(
                source_currency=source_currency,
                exchanged_currency=exchanged_currency,
                valuation_date=valuation_date,
                rate_value=rate_value,
            )

            self.stdout.write(
                self.style.SUCCESS(
                    "Updated exchange rate for {}/{} pair with date:{} and provider:{}".format(
                        source_currency,
                        exchanged_currency,
                        valuation_date,
                        provider,
                    )
                )
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR("Error fetching rates"))
            raise CommandError(e)