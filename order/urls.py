from django.urls import path
from .views import (hello,create_order,add_to_cart,empty_cart,update_item,mark_order_paid,
                    get_cart,remove_from_cart,cart_checkout,get_customer_orders,generate_delivery_otp,
    confirm_delivery_otp,cancel_order,get_order_detail,get_orders_staff,update_orders_staff,get_delivery_orders,update_status_delivery,order_report)

urlpatterns=[
    path("hello/",hello),
    path("create_order/",create_order),
    path("staff/orders/",get_orders_staff),
    path("delivery/orders/",get_delivery_orders),
    path("delivery/update/order/<int:order_id>/",update_status_delivery),
    path("delivery/generate_otp/<int:order_id>/", generate_delivery_otp),
    path("delivery/confirm_otp/<int:order_id>/", confirm_delivery_otp),
    path("staff/update/<int:order_id>/",update_orders_staff),
  
    path("customer/orders/",get_customer_orders),
    path("cancel/<int:order_id>/",cancel_order),
    path("get_cart/",get_cart),
    path("add_to_cart/",add_to_cart),
    path("remove_from_cart/<int:order_item_id>/",remove_from_cart),
    path("empty_cart/",empty_cart),
    path("checkout_cart/",cart_checkout),
    path("update_item/<int:item_id>/",update_item),
    path('mark_order_paid/<int:order_id>/',mark_order_paid),
    path('order-report/',order_report),
    path("detail/<int:order_id>/", get_order_detail),

]