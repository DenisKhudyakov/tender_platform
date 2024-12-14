from datetime import date

from django import forms
from django.forms import modelformset_factory
from rest_framework.exceptions import ValidationError

from .models import AnswerOnOrder, Order, OrderProduct, PriceAnalysis, Product


class ProductForm(forms.ModelForm):
    """
    Форма создания продукта
    """
    class Meta:
        model = Product
        fields = ["name", "article", "measurement"]


class DateInput(forms.DateInput):
    """
    Форма даты
    """
    input_type = "date"


class OrderForm(forms.ModelForm):
    """
    Форма создания пустого заказа
    """
    class Meta:
        model = Order
        fields = ["number_ERP", "description", "duration", "is_active"]
        widgets = {
            "number_ERP": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "duration": DateInput(attrs={"class": "form-control", "type": "date"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        help_texts = {
            "description": "Создайте заявку, чтобы в дальнейшем добавить в неё товары",
        }

    def clean_duration(self):
        duration = self.cleaned_data.get("duration")
        if duration and duration < date.today():
            raise ValidationError("Дата не может быть в прошлом.")
        return duration


class OrderProductForm(forms.ModelForm):
    """
    Форма создания заказа с товарами
    """
    class Meta:
        model = OrderProduct
        fields = ["amounts"]


class AnswerOnOrderForm(forms.ModelForm):
    """
    Форма ответа на заказ
    """
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
    """
    Форма анализа цен, опционально, не использовалось в проекте
    """
    class Meta:
        model = PriceAnalysis
        fields = ["order", "answer"]


class FilterForm(forms.Form):
    """
    Форма для фильтрации заказов
    """
    search = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите номер заказа"}
        ),
        label="Поиск",
    )


class FilterProductForm(FilterForm):
    """
    Форма для фильтрации продуктов
    """
    search = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите артикул"}
        ),
        required=False,
        max_length=100,
        label="Поиск",
    )
