from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from ..models import Order
from ..serializers.order import OrderSerializer
from ..services.order_service import OrderService
from ..filters import OrderFilter

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_all_orders(request):
    orders = Order.objects.all()
    filtered_orders = OrderFilter(request.GET, queryset=orders).qs
    serializer = OrderSerializer(filtered_orders, many=True)
    return Response({'orders': serializer.data})

@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def process_order(request, pk):
    try:
        order = Order.objects.get(id=pk)
        updated_order = OrderService.update_order_status(order, request.data['status'])
        serializer = OrderSerializer(updated_order)
        return Response({'order': serializer.data})
    except Order.DoesNotExist:
        return Response(
            {'error': 'الطلب غير موجود'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )