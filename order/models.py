from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from django.db.models import Sum, F
from django.forms import ValidationError
from product.models import Product

User = get_user_model()

class OrderStatus(models.TextChoices):
    PROCESSING = 'Processing', 'قيد المعالجة'
    SHIPPED = 'Shipped', 'تم الشحن'
    DELIVERED = 'Delivered', 'تم التوصيل'
    CANCELLED = 'Cancelled', 'ملغي'
    RETURNED = 'Returned', 'تم الإرجاع'

class PaymentStatus(models.TextChoices):
    PAID = 'Paid', 'مدفوع'
    UNPAID = 'Unpaid', 'غير مدفوع'
    REFUNDED = 'Refunded', 'تم الاسترجاع'
    PARTIALLY_REFUNDED = 'Partially_Refunded', 'تم استرجاع جزء'

class PaymentMode(models.TextChoices):
    COD = 'COD', 'الدفع عند الاستلام'
    CARD = 'CARD', 'بطاقة ائتمان'
    TRANSFER = 'Transfer', 'حوالة بنكية'
    WALLET = 'Wallet', 'محفظة إلكترونية'

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='orders',verbose_name='المستخدم')
    city = models.CharField(max_length=400, verbose_name='المدينة')
    zip_code = models.CharField(max_length=100, verbose_name='الرمز البريدي')
    street = models.CharField(max_length=500, verbose_name='الشارع')
    state = models.CharField(max_length=100, verbose_name='المنطقة')
    country = models.CharField(max_length=100, verbose_name='الدولة')
    phone_no = models.CharField(max_length=100, verbose_name='رقم الهاتف')
    total_amount = models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0)],verbose_name='المبلغ الإجمالي',default=0)
    payment_status = models.CharField(max_length=30,choices=PaymentStatus.choices,default=PaymentStatus.UNPAID,verbose_name='حالة الدفع')
    payment_mode = models.CharField(max_length=30,choices=PaymentMode.choices,default=PaymentMode.COD,verbose_name='طريقة الدفع')
    status = models.CharField(max_length=60,choices=OrderStatus.choices,default=OrderStatus.PROCESSING,verbose_name='حالة الطلب')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')
    notes = models.TextField(blank=True, null=True, verbose_name='ملاحظات')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'طلب'
        verbose_name_plural = 'الطلبات'
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['payment_status']),
        ]

    def __str__(self):
        return f"Order #{self.id} - {self.user.email if self.user else 'No User'}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items',verbose_name='الطلب')
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,related_name='order_items',verbose_name='المنتج')
    name = models.CharField(max_length=200, verbose_name='الاسم')
    quantity = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1)],verbose_name='الكمية')
    price = models.DecimalField(max_digits=7,decimal_places=2,validators=[MinValueValidator(0)],verbose_name='السعر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')

    class Meta:
        verbose_name = 'عنصر الطلب'
        verbose_name_plural = 'عناصر الطلب'
        indexes = [
            models.Index(fields=['order', 'product']),
            models.Index(fields=['product']),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(quantity__gte=1),name='quantity_gte_1'),
            models.CheckConstraint(check=models.Q(price__gte=0),name='price_gte_0'),
        ]
    def save(self, *args, **kwargs):
        if self.order.status not in [OrderStatus.PROCESSING]:
            raise ValidationError("لا يمكن تعديل العنصر بعد اكتمال الطلب")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.order.status not in [OrderStatus.PROCESSING]:
            raise ValidationError("لا يمكن حذف العنصر بعد اكتمال الطلب")
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (x{self.quantity}) - {self.order}"
