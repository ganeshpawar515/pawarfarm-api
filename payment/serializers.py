# payment/serializers.py
from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    driver = serializers.CharField(source="user.username", read_only=True)
    related_order = serializers.CharField(source="related_order.id", read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'driver', 'related_order', 'amount', 'status', 'paid_at']
