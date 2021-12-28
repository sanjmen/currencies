from rest_framework import viewsets
from .serializers import MarketSerializer, KlineSerializer

from apps.markets.models import Market, Kline

# ViewSets define the view behavior.
class MarketsViewSet(viewsets.ModelViewSet):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer


class KlinesViewSet(viewsets.ModelViewSet):
    queryset = Kline.objects.all().select_related("market")
    serializer_class = KlineSerializer

    def get_queryset(self):
        queryset = Kline.objects.all().select_related("market")

        symbol = self.request.query_params.get("symbol")
        if symbol is not None:
            queryset = queryset.filter(market__symbol__iexact=symbol)

        return queryset