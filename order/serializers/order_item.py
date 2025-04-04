from rest_framework import serializers

from product.models import Product
from ..models import OrderItem, OrderStatus

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        read_only_fields = ('name', 'price','created_at')
        
    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("الكمية يجب أن تكون على الأقل 1")
        return value
    
    def validate(self, data):
        if self.instance.order.status != OrderStatus.PROCESSING:
            raise serializers.ValidationError(
                "لا يمكن تعديل العنصر بعد بدء معالجة الطلب"
            )
        product = Product.objects.get(id=data['product_id'])
        if float(data['price']) != float(product.price):
            raise serializers.ValidationError(
                {"price": f"سعر المنتج لا يتطابق. السعر الحقيقي: {product.price}"}
            )
        return data
