from django import forms
from django.forms import formset_factory, modelformset_factory

from .models import AnswerOnOrder, Order, OrderProduct, PriceAnalysis, Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "article", "measurement"]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []
        help_texts = "Создайте заявку, чтобы в дальнейшем добавить в неё товары"


class OrderProductForm(forms.ModelForm):
    class Meta:
        model = OrderProduct
        fields = ["amounts"]


class AnswerOnOrderForm(forms.ModelForm):
    class Meta:
        model = AnswerOnOrder
        fields = ["order_product", "price", "delivery_time"]
        widgets = {
            "id": forms.HiddenInput(),
            "price": forms.TextInput(attrs={"class": "form-control"}),
            "delivery_time": forms.TextInput(attrs={"class": "form-control"}),
            "order_product": forms.HiddenInput(),
        }


AnswerOnOrderFormSet = modelformset_factory(
    AnswerOnOrder,
    form=AnswerOnOrderForm,
    extra=0,
)

ProductFormSet = modelformset_factory(Product, form=ProductForm, extra=10)


class PriceAnalysisForm(forms.ModelForm):
    class Meta:
        model = PriceAnalysis
        fields = ["order", "answer"]


class FilterForm(forms.Form):
    search = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите номер заказа"}
        ),
        label="Поиск",
    )
