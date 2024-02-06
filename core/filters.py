import django_filters
from .models import Property, Booking


class PropertyFilter(django_filters.FilterSet):
    """Django filter for property model"""

    name = django_filters.CharFilter(lookup_expr="icontains")
    """Filter properties by name with case insensitive search"""
    min_price = django_filters.NumberFilter(field_name="base_price", lookup_expr="gte")
    """Filter for base price greater than or equal to given value"""
    max_price = django_filters.NumberFilter(field_name="base_price", lookup_expr="lte")
    """Filter for base price less than or equal to given value"""

    class Meta:
        """Meta class for property filter"""

        model = Property
        fields = ["name", "min_price", "max_price"]


class BookingFilter(django_filters.FilterSet):
    date_start = django_filters.DateFilter(field_name="date_start")
    date_end = django_filters.DateFilter(field_name="date_end")
    property = django_filters.NumberFilter(field_name="property")

    class Meta:
        model = Booking
        fields = ["date_start", "date_end", "property"]
