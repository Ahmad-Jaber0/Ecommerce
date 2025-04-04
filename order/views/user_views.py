from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..models import Order
from ..serializers.order import OrderSerializer
from ..services.order_service import OrderService
from ..filters import OrderFilter

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_orders(request):
    orders = OrderService.get_user_orders(request.user)
    filtered_orders = OrderFilter(request.GET, queryset=orders).qs
    serializer = OrderSerializer(filtered_orders, many=True)
    return Response({'orders': serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    try:
        order = OrderService.create_order(request.user, request.data)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_details(request, pk):
    try:
        order = Order.objects.get(id=pk, user=request.user)
        serializer = OrderSerializer(order)
        return Response({'order': serializer.data})
    except Order.DoesNotExist:
        return Response(
            {'error': 'الطلب غير موجود أو ليس لديك صلاحية الوصول'},
            status=status.HTTP_404_NOT_FOUND
        )