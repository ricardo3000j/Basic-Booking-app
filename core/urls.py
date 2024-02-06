from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, PricingRuleViewSet, BookingViewSet

# from .views import BookViewSet
router = DefaultRouter()
router.register(r'properties', PropertyViewSet)
router.register(r'pricerules', PricingRuleViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
