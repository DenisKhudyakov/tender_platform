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
        {"name": "Продукт 1", "article": "ART001", "measurement": "кг"},
        {"name": "Продукт 2", "article": "ART002", "measurement": "шт"}
    ],
    "amounts": [10.5, 3.2]
    }
    """
    def post(self, request, *args, **kwargs):
        serializer = OrderProductCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        return Response(
            {"order_id": order.id, "message": "Заявка для поставщиков успешно создана"},
            status=status.HTTP_201_CREATED
        )

