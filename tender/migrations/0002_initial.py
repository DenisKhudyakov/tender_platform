# Generated by Django 5.1.3 on 2024-11-23 11:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("tender", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="answeronorder",
            name="supplier",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="suppliers",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Поставщики",
            ),
        ),
        migrations.AddField(
            model_name="orderproduct",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to="tender.order",
                verbose_name="Заявка",
            ),
        ),
        migrations.AddField(
            model_name="answeronorder",
            name="order_product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="order_product",
                to="tender.orderproduct",
                verbose_name="Заявка",
            ),
        ),
        migrations.AddField(
            model_name="priceanalysis",
            name="answer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="answers",
                to="tender.answeronorder",
                verbose_name="Ответ на заявку",
            ),
        ),
        migrations.AddField(
            model_name="priceanalysis",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="price_analysis_orders",
                to="tender.order",
                verbose_name="Заявки",
            ),
        ),
        migrations.AddField(
            model_name="orderproduct",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="products",
                to="tender.product",
                verbose_name="Продукты",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="product",
            field=models.ManyToManyField(
                help_text="Товары в заявке",
                related_name="order_products",
                through="tender.OrderProduct",
                to="tender.product",
            ),
        ),
    ]
