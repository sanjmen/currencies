from django.db import models
from django.db.models.fields import IntegerField

from .fields import AmountField, PriceField


class Interval(models.TextChoices):
    MINUTE = "1m"
    HOUR = "1h"
    DAY = "1d"

class Status(models.TextChoices):
    TRADING = "TRADING"
    BREAK = "BREAK"


class Market(models.Model):
    symbol = models.CharField(max_length=20, db_index=True, default="BTC/USDT")
    status = models.CharField(choices=Status.choices, default=Status.TRADING, max_length=7, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.symbol


class Kline(models.Model):
    """
    [
        1499040000000,      // Open time
        "0.01634790",       // Open
        "0.80000000",       // High
        "0.01575800",       // Low
        "0.01577100",       // Close
        "148976.11427815",  // Volume
    ]
    """

    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    interval = models.CharField(
        max_length=2, choices=Interval.choices, default=Interval.MINUTE, db_index=True
    )

    open_time = models.DateTimeField(db_index=True)

    open = PriceField()
    high = PriceField()
    low = PriceField()
    close = PriceField()

    volume = AmountField()

    class Meta:
        ordering = ["-open_time"]
        unique_together = ("market", "interval", "open_time")
        indexes = [
            models.Index(fields=["open_time", "market", "interval"]),
            models.Index(fields=["-open_time"], name="open_time_idx"),
        ]

    def __str__(self):
        return "{0.market.symbol} {0.close} {0.open_time}>".format(self)