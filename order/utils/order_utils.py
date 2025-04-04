from django.db import transaction
from  product.models import Product

def lock_product_stock(product_id):
    
    #(Race Condition)
    product = Product.objects.select_for_update().get(id=product_id)
    return product

def calculate_order_total(items):

    return sum(item['price'] * item['quantity'] for item in items)