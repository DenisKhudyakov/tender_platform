from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.forms import formset_factory
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  UpdateView)

from tender.forms import (AnswerOnOrderForm, AnswerOnOrderFormSet, FilterForm,
                          OrderForm, OrderProductForm, PriceAnalysisForm,
                          ProductForm, ProductFormSet)
from tender.models import (AnswerOnOrder, Order, OrderProduct, PriceAnalysis,
                           Product)
from users.models import User


class OrderListView(ListView):
    model = Order
    context_object_name = "orders"


class OrderDetailView(DetailView):
    model = Order
    template_name = "tender/order_detail.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        order = self.object.pk
        context["products"] = OrderProduct.objects.filter(order=order)
        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("tender:questions")


def questions_for_products(request):
    return render(request, template_name="tender/questions_for_product.html")


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    context_object_name = "orders"
    template_name = "tender/order_form.html"

    def form_valid(self, form):
        order = form.save()
        return redirect(reverse("tender:order_detail", args=[order.id]))


class ProductListView(ListView):
    model = Product
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["order_pk"] = self.kwargs["pk"]
        context["form"] = OrderProductForm()
        return context

    def post(self, request, *args, **kwargs):
        order_pk = self.kwargs["pk"]
        order = get_object_or_404(Order, pk=order_pk)
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, pk=product_id)
        form = OrderProductForm(request.POST)

        if form.is_valid():
            # Создаем или обновляем запись в OrderProduct
            order_product, created = OrderProduct.objects.get_or_create(
                order=order,
                product=product,
                defaults={"amounts": form.cleaned_data["amounts"]},
            )
            if not created:  # Если запись уже существует, обновляем количество
                order_product.amounts += form.cleaned_data["amounts"]
                order_product.save()
        return redirect("tender:product_list", pk=order_pk)


class OrderProductListView(ListView):
    model = OrderProduct
    context_object_name = "order_products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = FilterForm(self.request.GET or None)
        context["form"] = form
        return context

    def get_queryset(self):
        queryset = super().get_queryset().distinct("order")
        form = FilterForm(self.request.GET or None)
        if form.is_valid():
            search = form.cleaned_data["search"]
            if search:
                queryset = queryset.filter(order__id__icontains=search)
        return queryset


class OrderProductDetailView(DetailView):
    model = OrderProduct
    context_object_name = "order_product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        order = self.object.order
        context["products"] = OrderProduct.objects.filter(order=order)
        context["has_answer"] = AnswerOnOrder.objects.filter(
            order_product__order=order, supplier=self.request.user
        ).exists()
        return context


def create_answer_on_order(request, pk):
    order = get_object_or_404(OrderProduct, pk=pk).order

    order_products = OrderProduct.objects.filter(order=order)

    AnswerOnOrderFormSet = formset_factory(
        AnswerOnOrderForm,
        extra=0,
    )

    if request.method == "POST":
        formset = AnswerOnOrderFormSet(request.POST)

        if formset.is_valid():
            for form in formset.forms:
                answer = form.save(commit=False)
                print(f"пользователь {request.user}")
                answer.supplier = (
                    request.user
                )  # Устанавливаем текущего пользователя как поставщика
                print(f"Поставщик загружен {answer.supplier}")
                answer.save()
            return redirect("tender:order_products")  # Перенаправление после сохранения
    else:

        initial_data = [{"order_product": product} for product in order_products]
        formset = AnswerOnOrderFormSet(initial=initial_data)
    context = {
        "formset": formset,
        "order": order,
        "order_products": order_products,
    }

    return render(request, "tender/answer_on_order.html", context)


def update_answer_on_order(request, pk):
    order = get_object_or_404(Order, pk=pk)

    answer = AnswerOnOrder.objects.filter(
        order_product__order=order, supplier=request.user
    )

    if not answer.exists():
        return render(request, "tender/no_answers.html", {"order": order})

    if request.method == "POST":
        formset = AnswerOnOrderFormSet(request.POST, queryset=answer)
        if formset.is_valid():
            formset.save()
            return render(
                request, "tender/update_answers_success.html", {"order": order}
            )
        else:
            print(formset.errors)
    else:
        formset = AnswerOnOrderFormSet(queryset=answer)
    return render(
        request, "tender/update_answers.html", {"order": order, "formset": formset}
    )


class AnswerOnOrderListView(LoginRequiredMixin, ListView):
    """
    Контроллер анализа цен, выводим все ответы на заявку по номеру заявки
    """

    model = AnswerOnOrder
    template_name = "tender/price_analysis.html"

    def get_queryset(self):
        pk = self.kwargs["pk"]
        try:
            order = Order.objects.get(pk=pk)
            return AnswerOnOrder.objects.filter(
                order_product__order=order
            ).select_related("supplier")
        except Order.DoesNotExist:
            raise Http404("Заказ не найден")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # важно передать **kwargs
        order_answers = self.get_queryset()
        context["order_answers"] = order_answers  # более описательное имя
        unique_products = order_answers.values_list(
            "order_product__product__name", flat=True
        ).distinct()
        context["products"] = unique_products
        return context
