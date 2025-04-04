class InsufficientStockException(Exception):
    def __init__(self, product_name, available, requested):
        self.message = (
            f"لا يوجد مخزون كافي للمنتج {product_name}. "
            f"المتوفر: {available}, المطلوب: {requested}"
        )
        super().__init__(self.message)

class OrderValidationException(Exception):
    pass