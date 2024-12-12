from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import OrderProductCreateSerializer


class TestAPIView(APIView):
    """
    Тестовый запрос, для проверки работоспособности
    """

    def get(self, request):
        return Response({"message": "Hello World"})


class CreateOrderWithProductsView(APIView):
    """
    Контроллер создания заявки для поставщиков

    Тестовые данные
    {
    "products": [
        {"article": "12345", "name": "Product A", "measurement": "шт"},
        {"article": "67890", "name": "Product B", "measurement": "кг"}
    ],
    "amounts": [10, 20],
    "number_ERP": "ERP12345",
    "description": "Закупка товаров для проекта",
    "duration": "2024-12-31",
    }

    """

    def post(self, request, *args, **kwargs):
        serializer = OrderProductCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        return Response(
            {"order_id": order.id, "message": "Заявка для поставщиков успешно создана"},
            status=status.HTTP_201_CREATED,
        )
