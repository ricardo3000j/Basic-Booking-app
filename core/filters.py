import django_filters
from .models import Property


class PropertyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    min_price = django_filters.NumberFilter(field_name="base_price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="base_price", lookup_expr="lte")

    class Meta:
        model = Property
        fields = ["name", "min_price", "max_price"]
