from core.filters import PropertyFilter
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Property
from .serializers import PropertySerializer


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PropertyFilter
