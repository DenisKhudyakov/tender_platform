# Generated by Django 5.1.3 on 2024-11-11 12:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tender", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderproduct",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to="tender.order",
                verbose_name="Заявка",
            ),
        ),
        migrations.AlterField(
            model_name="orderproduct",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="products",
                to="tender.product",
                verbose_name="Продукты",
            ),
        ),
    ]
