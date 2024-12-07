from django.urls import path
from api.views import TestAPIView, CreateOrderWithProductsView
from api.apps import ApiConfig

app_name = ApiConfig.name

urlpatterns = [
    path('test/', TestAPIView.as_view(), name='test'),
    path('create-order-products/', CreateOrderWithProductsView.as_view(), name='create-order-products'),
]