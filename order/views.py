from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import Order,OrderItem
from user.permissions import IsStaffUser
from django.core.exceptions import ValidationError


@api_view(["GET"])
def hello(request):
    return Response({"message Hello"})


   

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields=['id','order','product','product_name','quantity','price']
        read_only_fields=['price']
        extra_kwargs={
            'product':{'required':True,'allow_null':False}
        }
class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True,read_only=True)
    is_paid=serializers.BooleanField(read_only=True)
    username=serializers.SerializerMethodField()
    class Meta:
        model=Order
        fields=['id','username','assigned_driver','assigned_driver_name','status','created_at','total_price','payment_mode','items','is_paid']
        read_only_fields=['assigned_driver_name','user','total_price','created_at']

    def validate_is_paid(self, value):
        user = self.context['request'].user
        if not user.is_staff:
            raise serializers.ValidationError("Only Staff Can Update Payment Status")
        if self.instance and self.instance.status=="draft" and value is True:
            raise serializers.ValidationError("Darft cannot be marked as paid")
        return value
    def get_username(self,obj):
        return obj.user.username if obj.user else None


@api_view(["POST"])
@permission_classes([IsStaffUser])
def mark_order_paid(request,order_id):
    try:
        order=Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({'error':'Order Not Found'})
    try:
        order.is_paid=True
        order.save()
    except ValidationError:
        return Response({"error":"not valid operation"})
    return Response({"message":f"Order {order.id} marked as paid"})



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_customer_orders(request):
    orders=Order.objects.filter(user=request.user).exclude(status="draft")
    serializer=OrderSerializer(orders,many=True)
    return Response(serializer.data)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def cancel_order(request,order_id):
    try:
        order = Order.objects.get(id=order_id)
        order.delete()
        return Response({"message":"Order Deleted Successfully"})
    except Order.DoesNotExist:
        return Response({"error":"Order not found"})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_order(request):
    data=request.data.copy()
    data['user']=request.user.id
    items=data.pop('items',[])
    order_serializer = OrderSerializer(data=data,context={"request":request})
    if order_serializer.is_valid():

        order=order_serializer.save(user=request.user)
    else:
        return Response(order_serializer.errors)
    for item in items:
        item['order']=order.id
        order_item_serializer=OrderItemSerializer(data=item,context={"request":request})
        if order_item_serializer.is_valid():

            order_item_serializer.save()
        else:
            order.delete()
            return Response({"message":order_item_serializer.errors})
    return Response(OrderSerializer(order, context={'request': request}).data)

import datetime
from django.utils import timezone
@api_view(["GET"])
@permission_classes([IsStaffUser])
def get_orders_staff(request):
    status = request.GET.get('status')
    date = request.GET.get('date')

    orders=Order.objects.all()
    if status:
        orders=orders.filter(status=status)
    if date:
        naive_date = datetime.datetime.strptime(date, "%Y-%m-%d")
        orders=orders.filter(created_at__date=timezone.make_aware(naive_date))
    serializer = OrderSerializer(orders,many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_delivery_orders(request):
    orders=Order.objects.filter(assigned_driver=request.user)
    serializer=OrderSerializer(orders,many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_status_delivery(request,order_id):
    try:
        order=Order.objects.get(id=order_id)
        if order.status=="delivered" or order.status=="cancelled":
            return Response({'error':"status update restricted"})
    except Order.DoesNotExist:
        return Response({"error":"Order not found"})
    data=request.data.copy()
    new_status=data.get("status")
    if new_status=='delivered':
        order.is_paid=True
    order.status=new_status
    order.save()
    return Response({"message":"updated"})
    


@api_view(["PUT","PATCH"])
@permission_classes([IsStaffUser])
def update_orders_staff(request,order_id):
    try:
        order=Order.objects.get(id=order_id)
        data=request.data
        print(data)
        serializer = OrderSerializer(order,data,partial=True)
        if serializer.is_valid():
            serializer.save()
            if order.assigned_driver and order.status=='pending':
                order.status='assigned'
                order.save()
                return Response({"error":"remove assigned driver to update status to pending"})
            if not order.assigned_driver:
                order.status='pending'
                order.save()
                return Response({'error':"driver not assigned yet"})

            return Response({"message":"order updated"})
        return Response({"error":"Order update failed"})
    except Order.DoesNotExist:
        return Response({"error":"Order not Found"})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    data = request.data.copy()
    items = data.pop('items',[])
    if not items:
        return Response({"Error":"Product must be selected"})
    
    order,created = Order.objects.get_or_create(user=request.user,status="draft")

    for item in items:
        item["order"]=order.id
        item_serializer = OrderItemSerializer(data=item,context={"request":request})
        if item_serializer.is_valid():
            item_serializer.save()
        else:
            return Response({"Error":item_serializer.errors})
    return Response({"message":"Added to cart"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cart(request):
    try:
        cart = Order.objects.get(user=request.user, status="draft")
    except Order.DoesNotExist:
        # Return empty cart data if no draft order exists
        return Response({"cart_data": None})
    
    serializer = OrderSerializer(cart)
    return Response({"cart_data": serializer.data})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request,order_item_id):
    try:
        item = OrderItem.objects.get(id=order_item_id)
        if item.order.user==request.user:
            order=item.order
            item.delete()
            order.update_total()
            return Response({"message":"item removed from cart",'total_price':order.total_price})
        else:
            return Response({"error":"wrong item id"})

    except OrderItem.DoesNotExist:
        return Response({"error":"item not found"})

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def empty_cart(request):
    
    try:
        cart=Order.objects.filter(user=request.user,status="draft")
        cart.delete()
        return Response({"message":"Cart emptied"})
    except Order.DoesNotExist:
        return Response({"error":"Cart already Empty"})
    
@api_view(["PUT","PATCH"])
@permission_classes([IsAuthenticated])
def update_item(request,item_id):
    try:
        item=OrderItem.objects.get(id=item_id)
        if item.order.user==request.user:
            serializer = OrderItemSerializer(item,data=request.data,context={"request":request},partial=True)
            if serializer.is_valid():
                serializer.save()
                item.order.update_total()
                return Response({"message":f"Item updated to {serializer.data}",'total_price':item.order.total_price})
            else:
                return Response({"error":serializer.errors})
        else:
            return Response({"error":"Invalid User for item"})
            
    except OrderItem.DoesNotExist:
        return Response({"message","Item not found"})


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .models import Order
from django.db.models import Count, Sum, Q
from datetime import datetime, timedelta

@api_view(["GET"])
@permission_classes([IsAdminUser])
def order_report(request):
    total_orders = Order.objects.exclude(status="draft").count()
    delivered_orders = Order.objects.filter(status="delivered").count()
    pending_orders = Order.objects.filter(status="pending").count()
    assigned_orders = Order.objects.filter(status="assigned").count()
    on_way_orders = Order.objects.filter(status="on_way").count()
    cancelled_orders = Order.objects.filter(status="cancelled").count()
    total_revenue = Order.objects.filter(status="delivered").aggregate(
        total=Sum("total_price")
    )["total"] or 0

    # Orders in the last 7 days
    today = datetime.now().date()
    last_7_days = [
        (today - timedelta(days=i)) for i in range(6, -1, -1)
    ]
    orders_per_day = []
    for day in last_7_days:
        count = Order.objects.filter(
            created_at__date=day
        ).exclude(status="draft").count()
        orders_per_day.append({"date": day.strftime("%Y-%m-%d"), "count": count})

    return Response({
        "total_orders": total_orders,
        "delivered_orders": delivered_orders,
        "pending_orders": pending_orders,
        "assigned_orders": assigned_orders,
        "on_way_orders": on_way_orders,
        "cancelled_orders": cancelled_orders,
        "total_revenue": float(total_revenue),
        "orders_per_day": orders_per_day,
    })