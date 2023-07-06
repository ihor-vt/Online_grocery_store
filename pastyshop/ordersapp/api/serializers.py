from rest_framework import serializers

from ordersapp.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "price", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "address",
            "postal_code",
            "city",
            "created",
            "updated",
            "paid",
            "stripe_id",
            "coupon",
            "discount",
            "items",
        ]
