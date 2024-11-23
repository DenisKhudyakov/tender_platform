from django import forms
from django.forms import modelformset_factory

from .models import Product, Order, OrderProduct, AnswerOnOrder


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


class AnswerOnOrderForm(forms.ModelForm):
    class Meta:
        model = AnswerOnOrder
        fields = ['order_product', 'price', 'delivery_time']
        widgets = {
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'delivery_time': forms.TextInput(attrs={'class': 'form-control'}),
            'order_product': forms.HiddenInput()
        }



