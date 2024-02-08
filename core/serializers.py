from rest_framework import serializers
from .models import Property, PricingRule, Booking
from datetime import timedelta


class PropertySerializer(serializers.ModelSerializer):
    """Serializer for property model
    fields to validate: id, name, base_price
    """

    class Meta:
        model = Property
        fields = ["id", "name", "base_price"]


class PricingRuleSerializer(serializers.ModelSerializer):
    """Serializer for pricing rule model
    fields to validate: property, price_modifier,
    min_stay_length, fixed_price, specific_day
    """

    class Meta:
        model = PricingRule
        fields = [
            "id",
            "property",
            "price_modifier",
            "min_stay_length",
            "fixed_price",
            "specific_day",
        ]


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for booking model
    fields to validate: property, date_start, date_end
    methods: create - create new booking instance and
    Calculate the final price based on the pricing rules of the property
    """

    final_price = serializers.FloatField(read_only=True)

    class Meta:
        model = Booking
        fields = ["id", "property", "date_start", "date_end", "final_price"]

    def create(self, validated_data) -> Booking:
        """Create new booking instance and
        Calculate the final price based on the pricing rules of the property
        """

        booking = Booking.objects.create(**validated_data)
        date_range = [
            booking.date_start + timedelta(days=i)
            for i in range((booking.date_end - booking.date_start).days + 1)
        ]
        total_price = 0
        for date in date_range:
            # Get all pricing rules for the property that apply to this date
            pricing_rules = PricingRule.objects.filter(
                property=booking.property, specific_day=date
            )

            # If no specific_day rules, get min_stay_length rules
            if not pricing_rules.exists():
                pricing_rules = PricingRule.objects.filter(
                    property=booking.property,
                    min_stay_length__lte=(booking.date_end - booking.date_start).days
                    + 1,
                )

            # If there are still no rules, set the base price and continue to next date
            if not pricing_rules.exists():
                total_price += booking.property.base_price
                continue

            # Sort the rules by fixed_price and price_modifier (descending order)
            pricing_rules = pricing_rules.order_by("-fixed_price", "-price_modifier")

            # Get the most relevant rule
            rule = pricing_rules.first()

            # Calculate the price for this date
            if rule.fixed_price is not None and date == rule.specific_day:
                price = rule.fixed_price
            elif rule.price_modifier is not None:
                price = booking.property.base_price * (1 + rule.price_modifier / 100)
            else:
                price = booking.property.base_price

            # Add the price to the total price
            total_price += price

        # Set the final price of the booking
        booking.final_price = total_price
        booking.save()
        return booking
