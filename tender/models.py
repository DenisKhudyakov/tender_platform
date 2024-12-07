from django.db import models

from users.models import NULLABLE, User


class Product(models.Model):
    """
    Модель товара
    """

    name = models.CharField(
        max_length=255, verbose_name="Товар", help_text="Название товара, обязательное поле"
    )
    article = models.CharField(
        max_length=255, verbose_name="Артикул", help_text="Артикул товара, должен быть уникальным", **NULLABLE
    )
    measurement = models.CharField(max_length=10, verbose_name='Единица измерения', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Order(models.Model):
    """
    Модель заявки, в которой может быть много товаров.
    """

    product = models.ManyToManyField(
        Product,
        through="OrderProduct",
        related_name="order_products",
        help_text="Товары в заявке",
    )

    def __str__(self):
        return f"Заявка {self.id}"

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"


class OrderProduct(models.Model):
    """
    Смежная таблица заявок и продуктов
    """

    order = models.ForeignKey(Order, related_name="orders", on_delete=models.CASCADE, verbose_name='Заявка')
    product = models.ForeignKey(
        Product, related_name="products", on_delete=models.CASCADE, verbose_name='Продукты'
    )
    amounts = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Количество", help_text="Количество товара в заявке", **NULLABLE
    )

    def __str__(self):
        return f"{self.order}, товар: {self.product.article} - {self.product.name}: {self.amounts}"

    class Meta:
        verbose_name = "Товар в заявке"
        verbose_name_plural = "Товары в заявке"


class AnswerOnOrder(models.Model):
    """
    Модель ответов на заявку.
    """
    supplier = models.ForeignKey(
        User,
        related_name="suppliers",
        verbose_name="Поставщики",
        on_delete=models.SET_NULL,
        null=True,
    )
    order_product = models.ForeignKey(
        OrderProduct, related_name='order_product', on_delete=models.CASCADE, verbose_name='Заявка',
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена", help_text="Стоимость товара, в рублях", default=0
    )
    delivery_time = models.CharField(
        max_length=255, verbose_name="Срок поставки", help_text="Срок поставки", default=0
    )

    def __str__(self):
        return f"номер заявки{self.order_product.order.pk}, Поставщик {self.supplier} - {self.order_product.product.name}"

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


class PriceAnalysis(models.Model):
    """
    Модель анализа цен
    """

    order = models.ForeignKey(
        Order,
        related_name="price_analysis_orders",
        on_delete=models.CASCADE,
        verbose_name="Заявки",
    )
    answer = models.ForeignKey(
        AnswerOnOrder,
        related_name="answers",
        on_delete=models.CASCADE,
        verbose_name="Ответ на заявку",
    )

    def __str__(self):
        return f"Анализ цен на заявку {self.order.id}"

    class Meta:
        verbose_name = "Анализ цен"
        verbose_name_plural = "Анализы цен"
