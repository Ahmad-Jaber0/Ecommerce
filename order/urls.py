from django.urls import path
from .views.user_views import (get_user_orders,create_order,get_order_details)
from .views.admin_views import (get_all_orders,process_order)

urlpatterns = [
    path('user/orders/', get_user_orders, name='user-orders-list'),
    path('user/orders/create/', create_order, name='create-order'),
    path('user/orders/<int:pk>/', get_order_details, name='order-details'),
    
    path('admin/orders/', get_all_orders, name='admin-orders-list'),
    path('admin/orders/<int:pk>/process/', process_order, name='process-order'),
]