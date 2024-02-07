from core.filters import PropertyFilter, BookingFilter
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Property, PricingRule, Booking
from .serializers import PricingRuleSerializer, PropertySerializer, BookingSerializer


class PropertyViewSet(viewsets.ModelViewSet):
    """CRUD operations for property model based on viewset"""

    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PropertyFilter


class PricingRuleViewSet(viewsets.ModelViewSet):
    """CRUD operations for PricingRule model based on viewset"""

    queryset = PricingRule.objects.all()
    serializer_class = PricingRuleSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """CRUD operations for Booking model based on viewset"""

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookingFilter
