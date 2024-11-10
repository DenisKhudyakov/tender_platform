from django.contrib import admin

from tender.models import (AnswerOnOrder, Order, OrderProduct, PriceAnalysis,
                           Product)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "article",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "get_products")

    def get_products(self, obj):
        return ",\n".join([product.name for product in obj.product.all()])

    get_products.short_description = "Продукты"


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "amounts")


@admin.register(AnswerOnOrder)
class AnswerOnOrderAdmin(admin.ModelAdmin):
    list_display = ("order", "supplier", "product", "price", "delivery_time")


@admin.register(PriceAnalysis)
class PriceAnalysisAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "answer",
        "get_product_and_price",
    )

    def get_product_and_price(self, obj):
        return obj.answer.product, obj.answer.price, obj.answer.delivery_time
