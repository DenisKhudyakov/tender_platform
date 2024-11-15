from django import forms
from django.forms import modelformset_factory

from .models import Product, Order, OrderProduct


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'article', 'measurement']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []


class OrderProductForm(forms.ModelForm):
    class Meta:
        model = OrderProduct
        fields = ['amounts']


