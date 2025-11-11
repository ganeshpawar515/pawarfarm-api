from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Payment
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework import serializers
from rest_framework import viewsets, permissions
from .models import Payment
from .serializers import PaymentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by("-created_at")
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        payment = self.get_object()
        payment.status = "paid"
        payment.paid_at = now()
        payment.save()
        return Response({"message": "Payment marked as paid"})
@api_view(['GET'])
def hello(request):
    return Response({'message':'Hello, World!'})

# class PaymentSerializer(serializers.ModelSerializer):
#     related_order_id = serializers.IntegerField(source='related_order.id', read_only=True)

#     class Meta:
#         model = Payment
#         fields = ['id', 'amount', 'status', 'paid_at', 'related_order_id']
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_delivery_earnings(request):
    user = request.user
    payments = Payment.objects.filter(user=user)

    total_earnings = payments.aggregate(total=Sum('amount'))["total"] or 0
    total_paid = payments.filter(status="paid").aggregate(total=Sum('amount'))["total"] or 0
    total_pending = payments.filter(status="pending").aggregate(total=Sum('amount'))["total"] or 0

    serializer = PaymentSerializer(payments, many=True)

    return Response({
        "payments": serializer.data,
        "total_earnings": float(total_earnings),
        "total_paid": float(total_paid),
        "total_pending": float(total_pending),
    })

    
    return Response(serializer.data)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.db.models import Sum
from .models import Payment
from order.models import Order
from datetime import datetime, timedelta

@api_view(["GET"])
@permission_classes([IsAdminUser])
def payment_report(request):

    pending_payments = Payment.objects.filter(status="pending").count()
    paid_payments = Payment.objects.filter(status="paid").count()
    failed_payments = Payment.objects.filter(status="failed").count()

    total_driver_due = Payment.objects.filter(status="pending").aggregate(
        total=Sum("amount")
    )["total"] or 0
    total_driver_paid = Payment.objects.filter(status="paid").aggregate(
        total=Sum("amount")
    )["total"] or 0

    # Last 7 days driver payment stats
    today = datetime.now().date()
    last_7_days = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
    payments_per_day = []

    for day in last_7_days:
        count = Payment.objects.filter(
            created_at__date=day
        ).count()
        payments_per_day.append({
            "date": day.strftime("%Y-%m-%d"),
            "count": count,
        })

    return Response({
        "pending_payments": pending_payments,
        "paid_payments": paid_payments,
        "failed_payments": failed_payments,
        "total_driver_due": float(total_driver_due),
        "total_driver_paid": float(total_driver_paid),
        "payments_per_day": payments_per_day,
    })
