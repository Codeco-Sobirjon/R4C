from rest_framework import serializers
from apps.orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['robot_serial', 'quantity']
        read_only_fields = ['created', 'is_robot_available', 'email_sent']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value

    def create(self, validated_data):
        return Order.objects.create(**validated_data, customer=self.context.get('request').user)
