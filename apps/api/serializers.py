from rest_framework import serializers

from apps.markets.models import Market, Kline


class MarketSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Market
        fields = ["symbol", "status"]

class KlineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Kline
        fields = "__all__"
        depth = 1