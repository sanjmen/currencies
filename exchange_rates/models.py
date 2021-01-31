from django.db import models
from django.utils.module_loading import import_module


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=20, db_index=True)
    symbol = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "currencies"
        ordering = ["-symbol"]

    def __str__(self):
        return self.symbol


class CurrencyExchangeRate(models.Model):

    source_currency = models.ForeignKey(
        Currency, related_name="exchanges", on_delete=models.CASCADE
    )
    exchanged_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    valuation_date = models.DateField(db_index=True)
    rate_value = models.DecimalField(db_index=True, decimal_places=6, max_digits=18)

    class Meta:
        ordering = ["-valuation_date"]

    def __str__(self):
        return "{0.source_currency}/{0.exchanged_currency} : {0.rate_value}".format(
            self
        )


class ProviderManager(models.Manager):
    def default(self):
        return self.filter(priority=Provider.PRIORITY_DEFAULT)


class Provider(models.Model):
    PRIORITY_DEFAULT = "0"
    PRIORITY_HIGH = "1"
    PRIORITY_MEDIUM = "2"
    PRIORITY_LOW = "3"

    PRIORITIES = (
        (PRIORITY_DEFAULT, "default"),
        (PRIORITY_HIGH, "high"),
        (PRIORITY_MEDIUM, "medium"),
        (PRIORITY_LOW, "low"),
    )

    module_path = models.CharField(
        max_length=100,
        help_text="module path to import from. i.e: exchange_rates.providers.mock",
    )
    class_name = models.CharField(
        max_length=20,
        db_index=True,
        help_text="the name of the class that implements the provider adapter. i.e",
    )
    priority = models.CharField(max_length=1, choices=PRIORITIES, default=PRIORITY_LOW)

    objects = ProviderManager()

    def get_adapter(self):
        """Returns the adapter class to call the provider"""
        try:
            adapter_module = import_module(self.module_path)
            adapter_class = getattr(adapter_module, self.class_name)
            return adapter_class()
        except Exception as e:
            raise ImportError(e)

    def __str__(self):
        return self.class_name
