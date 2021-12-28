import logging

from django.utils import timezone
from django.db.utils import IntegrityError

from celery import shared_task

from .models import Market, Status, Interval, Kline
from .broker import Broker

logger = logging.getLogger(__name__)

@shared_task(ignore_resuls=True)
def update_markets():
    broker = Broker()
    try:
        markets_info = broker.get_markets()
        for symbol in markets_info:
            market = markets_info[symbol]

            try:
                m = Market.objects.get(symbol=symbol)
            except Market.DoesNotExist:
                m = Market()
                m.symbol = symbol

            m.status = getattr(Status, market['info']['status'])
            m.save()
    except Exception as e:
        logger.error(e)


@shared_task(ignore_result=True)
def update_klines(symbol=None, interval=Interval.MINUTE):

    if symbol is None:
        for market in Market.objects.filter(status=Status.TRADING):
            update_klines.delay(market.symbol)

    try:
        market = Market.objects.get(symbol=symbol)
    except Market.DoesNotExist:
        return

    if market.status != Status.TRADING:
        return

    broker = Broker()
    klines = broker.get_klines(market.symbol, interval)
    for line in klines:
        k = Kline()
        k.market = market
        k.interval = Interval.MINUTE
        k.open_time = timezone.datetime.fromtimestamp(line[0] / 1000, timezone.utc)
        k.open = line[1]
        k.high = line[2]
        k.low = line[3]
        k.close = line[4]
        k.volume = line[5]

        try:
            k.save()
        except IntegrityError:
            pass



