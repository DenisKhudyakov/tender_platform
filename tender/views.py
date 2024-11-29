from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView

from tender.forms import ProductForm, OrderForm, OrderProductForm, AnswerOnOrderForm, PriceAnalysisForm, \
    AnswerOnOrderFormSet
from tender.models import OrderProduct, Order, Product, AnswerOnOrder, PriceAnalysis


class OrderListView(ListView):
    model = Order
    template_name = "tender/order_list.html"
    context_object_name = 'orders'


class OrderDetailView(DetailView):
    model = Order
    template_name = "tender/order_detail.html"
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['products'] = self.object.product.all()
        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('tender:order_list')


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    context_object_name = 'order'
    template_name = 'tender/order_list.html'

    def form_valid(self, form):
        order = form.save()
        return redirect(reverse('tender:order_detail', args=[order.id]))


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['order_pk'] = self.kwargs['pk']
        context['form'] = OrderProductForm()
        return context

    def post(self, request, *args, **kwargs):
        order_pk = self.kwargs['pk']
        order = get_object_or_404(Order, pk=order_pk)
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        form = OrderProductForm(request.POST)

        if form.is_valid():
            # Создаем или обновляем запись в OrderProduct
            order_product, created = OrderProduct.objects.get_or_create(
                order=order,
                product=product,
                defaults={'amounts': form.cleaned_data['amounts']}
            )
            if not created:  # Если запись уже существует, обновляем количество
                order_product.amounts += form.cleaned_data['amounts']
                order_product.save()
        return redirect('tender:product_list', pk=order_pk)


class OrderProductListView(ListView):
    model = OrderProduct
    context_object_name = 'order_products'

    def get_queryset(self):
        return super().get_queryset().distinct('order')


class OrderProductDetailView(DetailView):
    model = OrderProduct
    context_object_name = 'order_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        order = self.object.order
        context['products'] = OrderProduct.objects.filter(order=order)
        return context


def create_answer_on_order(request, pk):
    order = get_object_or_404(OrderProduct, pk=pk).order

    order_products = OrderProduct.objects.filter(order=order)

    AnswerOnOrderFormSet = formset_factory(
        AnswerOnOrderForm,
        extra=0,
    )

    if request.method == 'POST':
        formset = AnswerOnOrderFormSet(request.POST)

        if formset.is_valid():
            for form in formset.forms:
                form.supplier = request.user  # Устанавливаем текущего пользователя как поставщика
                form.save()
            return redirect('tender:order_list')  # Перенаправление после сохранения
    else:

        initial_data = [{'order_product': product} for product in order_products]
        formset = AnswerOnOrderFormSet(initial=initial_data)
    context = {
        'formset': formset,
        'order': order,
        'order_products': order_products,
    }

    return render(request, 'tender/answer_on_order.html', context)


def update_answer_on_order(request, pk):
    order = get_object_or_404(Order, pk=pk)

    answer = AnswerOnOrder.objects.filter(order_product__order=order, supplier=request.user)

    if not answer.exists():
        return render(request, 'tender/no_answers.html', {'order': order})

    if request.method == 'POST':
        formset = AnswerOnOrderFormSet(request.POST, queryset=answer)
        if formset.is_valid():
            formset.save()
            return render(request, "tender/update_answers_success.html", {"order": order})
        else:
            print(formset.errors)
    else:
        formset = AnswerOnOrderFormSet(queryset=answer)
    return render(request, "tender/update_answers.html", {"order": order, "formset": formset})


class AnswerOnOrderListView(LoginRequiredMixin, ListView):
    """
    Контроллер анализа цен, выводим все ответы на заявку по номеру заявку
    """
    model = AnswerOnOrder

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        pk = self.kwargs['pk']
        answers = AnswerOnOrder.objects.filter(order_product__order__id=pk)
        context['answers'] = answers
        return context























