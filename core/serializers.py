from rest_framework import serializers
from .models import Property, PricingRule, Booking
from datetime import timedelta


class PropertySerializer(serializers.ModelSerializer):
    """Serializer for property model"""

    class Meta:
        model = Property
        fields = ["id", "name", "base_price"]


class PricingRuleSerializer(serializers.ModelSerializer):
    """Serializer for pricing rule model"""

    class Meta:
        model = PricingRule
        fields = [
            "property",
            "price_modifier",
            "min_stay_length",
            "fixed_price",
            "specific_day",
        ]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["property", "date_start", "date_end"]

    def create(self, validated_data):
        booking = Booking.objects.create(**validated_data)
        # Calculate the final price based on the pricing rules of the property
        date = booking.date_start
        booking.final_price = 0
        while date <= booking.date_end:
            # Get the most relevant rule for the date
            rule = (
                PricingRule.objects.filter(property=booking.property, specific_day=date)
                .order_by("-min_stay_length")
                .first()
            )
            if rule:
                if rule.fixed_price:
                    booking.final_price += rule.fixed_price
                else:
                    booking.final_price += booking.property.base_price * (
                        1 + rule.price_modifier / 100
                    )
            else:
                booking.final_price += booking.property.base_price
            date += timedelta(days=1)
        booking.save()
        return booking
