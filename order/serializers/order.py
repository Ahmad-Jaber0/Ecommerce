import re
from rest_framework import serializers
from ..models import Order, OrderStatus, PaymentStatus
from .order_item import OrderItemSerializer

class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField(read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('user', 'total_amount', 'created_at', 'updated_at')

    def get_items(self, obj):
        items = obj.items.all()
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data

    def validate(self, data):
        if 'status' in data and data['status'] == OrderStatus.CANCELLED:
            if self.instance and self.instance.payment_status == PaymentStatus.PAID:
                data['payment_status'] = PaymentStatus.REFUNDED
        return data
    
    def validate_phone_no(self, value):
        if not re.match(r'^\+?[0-9]{8,15}$', value):
            raise serializers.ValidationError("رقم الهاتف غير صالح")
        return value 