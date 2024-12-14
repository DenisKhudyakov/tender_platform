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
    number_ERP = serializers.CharField(
        max_length=15,
        required=False,
        allow_null=True,
        allow_blank=True,
        help_text="Номер заказа из 1С, не обязательное поле.",
    )
    description = serializers.CharField(
        max_length=255,
        required=False,
        allow_null=True,
        allow_blank=True,
        help_text="Краткое описание заявки.",
    )
    duration = serializers.DateField(
        required=False,
        allow_null=True,
        help_text="Крайняя дата получения ответов на заявку. Формат: ДД.ММ.ГГГГ.",
    )
    is_active = serializers.BooleanField(default=True, help_text="Актуальна ли заявка?")

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
        number_ERP = validated_data.pop("number_ERP", None)
        description = validated_data.pop("description", None)
        duration = validated_data.pop("duration", None)
        is_active = validated_data.pop("is_active", True)
        product_data = validated_data.pop("products")
        amounts = validated_data.pop("amounts")

        order = Order.objects.create(
            number_ERP=number_ERP,
            description=description,
            duration=duration,
            is_active=is_active,
        )

        for product_info, amount in zip(product_data, amounts):
            article = product_info.get("article")

            product, created = Product.objects.get_or_create(
                article=article, defaults=product_info
            )

            OrderProduct.objects.create(order=order, product=product, amounts=amount)

        return order
