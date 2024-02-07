from django.test import TestCase
from datetime import date

from core.serializers import BookingSerializer
from .models import Property, Booking, PricingRule


class BookingTestCase(TestCase):
    """Test case for booking model
    1. Create a property
    2. Create a booking
    3. Check if the booking price is correct
    """

    def setUp(self):
        """Create a property for testing"""
        self.property = Property.objects.create(base_price=10)

    def test_case_1(self):
        """Test Case 1 Property have a PriceRule 
        for min_stay_length of 7 days"""
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
        """Test Case 2 Property have two PriceRules for min_stay_length"""
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
        """Test Case 3 Property have two PriceRules 
        one for min_stay_length and one for specific_day"""
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
        """Test Case 4 Property does not have PriceRules at all"""
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
