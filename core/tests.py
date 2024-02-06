from django.test import TestCase
from datetime import date

from core.serializers import BookingSerializer
from .models import Property, Booking, PricingRule


class BookingTestCase(TestCase):
    def setUp(self):
        self.property = Property.objects.create(base_price=10)

    def test_case_1(self):
        PricingRule.objects.create(
            property=self.property, min_stay_length=7, price_modifier=-10
        )
        serializer = BookingSerializer(
            data={
                "property": self.property.id,
                "date_start": date(2022, 1, 1),
                "date_end": date(2022, 1, 10),
            }
        )
        if serializer.is_valid():
            booking = serializer.save()
            self.assertAlmostEqual(booking.final_price, 90)

    def test_case_2(self):
        PricingRule.objects.create(
            property=self.property, min_stay_length=7, price_modifier=-10
        )
        PricingRule.objects.create(
            property=self.property, min_stay_length=30, price_modifier=-20
        )
        serializer = BookingSerializer(
            data={
                "property": self.property.id,
                "date_start": date(2022, 1, 1),
                "date_end": date(2022, 1, 10),
            }
        )
        if serializer.is_valid():
            booking = serializer.save()
            self.assertAlmostEqual(booking.final_price, 90)

    def test_case_3(self):
        PricingRule.objects.create(
            property=self.property, min_stay_length=7, price_modifier=-10
        )
        PricingRule.objects.create(
            property=self.property, specific_day=date(2022, 1, 4), fixed_price=20
        )
        serializer = BookingSerializer(
            data={
                "property": self.property.id,
                "date_start": date(2022, 1, 1),
                "date_end": date(2022, 1, 10),
            }
        )
        if serializer.is_valid():
            booking = serializer.save()
            self.assertAlmostEqual(booking.final_price, 101)

    def test_case_4(self):
        serializer = BookingSerializer(
            data={
                "property": self.property.id,
                "date_start": date(2022, 1, 1),
                "date_end": date(2022, 1, 10),
            }
        )
        if serializer.is_valid():
            booking = serializer.save()
            self.assertAlmostEqual(booking.final_price, 100)
