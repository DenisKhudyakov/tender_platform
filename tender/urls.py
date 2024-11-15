from django.urls import path

from tender.apps import TenderConfig
from tender.views import OrderListView, OrderDetailView, ProductCreateView, OrderCreateView, ProductListView, \
    OrderProductCreateView

app_name = TenderConfig.name

urlpatterns = [
    path("", OrderListView.as_view(), name="order_list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path('product/create/', ProductCreateView.as_view(), name='create_product'),
    path('order/create/', OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/products/', ProductListView.as_view(), name='product_list'),
    path('order_product/create/', OrderProductCreateView.as_view(), name='order_product_create'),
]