from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Payment
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework import serializers
@api_view(['GET'])
def hello(request):
    return Response({'message':'Hello, World!'})

class PaymentSerializer(serializers.ModelSerializer):
    related_order_id = serializers.IntegerField(source='related_order.id', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'amount', 'status', 'paid_at', 'related_order_id']
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_delivery_earnings(request):
    user=request.user
    payments=Payment.objects.filter(user=user)
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)