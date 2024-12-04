# Generated by Django 5.1.3 on 2024-12-04 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tender", "0003_alter_product_article_alter_product_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="answeronorder",
            name="delivery_time",
            field=models.CharField(
                default=0,
                help_text="Срок поставки",
                max_length=255,
                verbose_name="Срок поставки",
            ),
        ),
        migrations.AlterField(
            model_name="answeronorder",
            name="price",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                help_text="Стоимость товара, в рублях",
                max_digits=10,
                verbose_name="Цена",
            ),
        ),
    ]
