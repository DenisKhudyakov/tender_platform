from decimal import Decimal

from psycopg2 import IntegrityError
from rest_framework import serializers

from tender.models import Order, OrderProduct, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["article", "name", "measurement"]


class OrderProductCreateSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)
    amounts = serializers.ListField(
        child=serializers.DecimalField(max_digits=10, decimal_places=2),
        help_text="Список количеств товаров (должен соответствовать количеству продуктов).",
    )

    def validate(self, attrs):
        products = attrs.get("products")
        amounts = attrs.get("amounts")

        if len(products) != len(amounts):
            raise serializers.ValidationError(
                "Количество товаров и их количества должны совпадать."
            )

        if not all(isinstance(amount, (int, float, Decimal)) for amount in amounts):
            raise serializers.ValidationError("Каждое количество должно быть числом.")

        return attrs

    def create(self, validated_data):
        order = Order.objects.create()
        product_data = validated_data.pop("products")
        amounts = validated_data.pop("amounts")

        for product_info, amount in zip(product_data, amounts):
            article = product_info.get("article")

            product, created = Product.objects.get_or_create(
                article=article, defaults=product_info
            )

            OrderProduct.objects.create(order=order, product=product, amounts=amount)

        return order
