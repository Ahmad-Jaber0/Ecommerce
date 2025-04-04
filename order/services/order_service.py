from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ValidationError
from ..models import Order, OrderItem
from product.models import Product
from ..utils.order_utils import calculate_order_total,lock_product_stock

class OrderService:
    @staticmethod
    def create_order(user, order_data):
        try:
            with transaction.atomic():
                order_items_data = order_data.pop('order_items', [])
                
                if not order_items_data:
                    raise ValidationError("لا يمكن إنشاء طلب بدون عناصر")
                

                total_amount = calculate_order_total(order_items_data)

                order = Order.objects.create(user=user,total_amount=total_amount,**order_data)

                for item_data in order_items_data:
                    product = lock_product_stock(item_data['product_id'])
                    if Decimal(str(item_data['price'])) != product.price:
                        raise ValidationError(
                            f"سعر المنتج {product.name} غير صحيح"
                        )
                    
                    if product.stock < item_data['quantity']:
                        raise ValidationError(f"لا يوجد مخزون كافي للمنتج {product.name}")
                    
                    OrderItem.objects.create(
                        product=product,
                        order=order,
                        name=product.name,
                        quantity=item_data['quantity'],
                        price=item_data['price']
                    )
                    
                    product.stock -= item_data['quantity']
                    product.save()

                return order
        except Exception as e:
            raise ValidationError(f"فشل إنشاء الطلب: {str(e)}")

    @staticmethod
    def get_user_orders(user):
        return Order.objects.filter(user=user).select_related('user').order_by('-created_at')


    @staticmethod
    def update_order_status(order, status):
        order.status = status
        order.save()
        return order