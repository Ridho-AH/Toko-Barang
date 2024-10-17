import django_filters
from .models import SupDebtHistory
from .models import CusDebtHistory

class SupDebtHistoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = SupDebtHistory
        fields = ['name']


class CusDebtHistoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = CusDebtHistory
        fields = ['name']