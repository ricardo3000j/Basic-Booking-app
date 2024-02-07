import django_filters
from .models import Property, Booking


class PropertyFilter(django_filters.FilterSet):
    """Django filters for property model"""

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
    """Django filters for booking model"""
    date_start = django_filters.DateFilter(field_name="date_start")
    """Filter for booking by start date"""
    date_end = django_filters.DateFilter(field_name="date_end")
    """Filter for booking by end date"""
    property = django_filters.NumberFilter(field_name="property")
    """Filter for booking based on property id"""

    class Meta:
        model = Booking
        fields = ["date_start", "date_end", "property"]
