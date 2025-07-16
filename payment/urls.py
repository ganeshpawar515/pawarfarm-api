from django.urls import path
from . import views

urlpatterns=[
    path('hello/',views.hello,name='hello'),
    path('delivery-earnings/',views.get_delivery_earnings,name='get_delivery_earnings')
]