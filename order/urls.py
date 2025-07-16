from django.urls import path
from .views import (hello,create_order,add_to_cart,empty_cart,update_item,mark_order_paid,
                    get_cart,remove_from_cart,get_customer_orders,cancel_order,get_orders_staff,update_orders_staff,get_delivery_orders,update_status_delivery,order_report)

urlpatterns=[
    path("hello/",hello),
    path("create_order/",create_order),
    path("add_to_cart/",add_to_cart),
    path("get_cart/",get_cart),
    path("staff/orders/",get_orders_staff),
    path("delivery/orders/",get_delivery_orders),
    path("delivery/update/order/<int:order_id>",update_status_delivery),
    path("staff/update/<int:order_id>/",update_orders_staff),
  
    path("customer/orders/",get_customer_orders),
    path("cancel/<int:order_id>/",cancel_order),
    path("remove_from_cart/<int:order_item_id>/",remove_from_cart),
    path("empty_cart/",empty_cart),
    path("update_item/<int:item_id>/",update_item),
    path('mark_order_paid/<int:order_id>/',mark_order_paid),
    path('order-report/',order_report)
]