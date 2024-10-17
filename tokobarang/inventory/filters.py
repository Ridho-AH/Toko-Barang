import django_filters
from .models import Stock
from .models import StockHistory

class StockFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Stock
        fields = ['name']


class StockHistoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = StockHistory
        fields = ['name']