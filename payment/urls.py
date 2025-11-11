from django.urls import path,include
from . import views
from rest_framework import routers
from payment.views import PaymentViewSet

router = routers.DefaultRouter()
router.register("payments", PaymentViewSet)

urlpatterns=[
    path('hello/',views.hello,name='hello'),
    path("api/", include(router.urls)),
    path("report/", views.payment_report, name="payment-report"),
    path('delivery-earnings/',views.get_delivery_earnings,name='get_delivery_earnings')
]