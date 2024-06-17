# orders/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer
from .publisher import publish_order_created


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        order_data = response.data
        publish_order_created({
            'order_id': order_data['id'],
            'product_id': order_data['product_id'],
            'quantity': order_data['quantity']
        })
        return response

    @action(detail=True, methods=['post'])
    def update_with_product_details(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
            product_details = request.data

            # Update order with product details
            order.product_name = product_details['name']
            order.product_price = product_details['price']
            order.save()

            return Response({"message": "Order updated with product details"}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
