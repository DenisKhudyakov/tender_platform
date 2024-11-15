from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView

from tender.forms import ProductForm, OrderForm, OrderProductForm
from tender.models import OrderProduct, Order, Product


class OrderListView(ListView):
    model = Order
    template_name = "tender/order_list.html"
    context_object_name = 'orders'


class OrderDetailView(DetailView):
    model = Order
    template_name = "tender/order_detail.html"
    context_object_name = 'order'


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
        return redirect('tender:order_detail', pk=order_pk)


class OrderProductCreateView(CreateView):
    model = OrderProduct
    form_class = OrderProductForm
    template_name = 'tender/order_detail.html'

    def form_valid(self, form):
        product_id = self.kwargs['pk']
        product = get_object_or_404(Product, pk=product_id)
        order_product = OrderProduct.objects.get_or_create(product=product,
                                                           defaults={'amounts': form.cleaned_data['amounts']})[0]
        return redirect('tender:order_detail', order_product.order.id)