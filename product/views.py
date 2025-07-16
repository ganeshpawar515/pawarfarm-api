from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import serializers
from .models import Product
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsStaffUser
# Create your views here.


@api_view(["GET"])
def hello(request):
    return Response({"message":"hello from product"})

class ProductSerializer(serializers.ModelSerializer):
    # image = serializers.ImageField(use_url=True)
    class Meta:
        model=Product
        fields="__all__"
        read_only_fields=['id']

@api_view(["POST"])
@permission_classes([IsStaffUser])
def create_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success":True,"message":"Product Created","data":serializer.data},status=201)
    else:
        return Response({"success":False,
            "message":"Product creation Failed",
            "error":serializer.errors},status=400)

@api_view(["GET"])
def get_products(request):
    products=Product.objects.filter(is_available=True)
    serializer= ProductSerializer(products,many=True, context={'request': request})
    return Response({"success":True,
        "message":"Products fetched successfully"
        ,"data":serializer.data},status=200)

@api_view(["GET"])
def get_product_detail(request,pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return Response({"success":False,
            "message": "product not found"},status=404)
    serializer = ProductSerializer(product,context={'request': request})
    return Response({"success":True,
        "data":serializer.data},status=200)

@api_view(["PUT","PATCH"])
@permission_classes([IsStaffUser])
def update_product(request,pk):
    try:
        product=Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return Response({"success":False,
                         "error":"product not found"},status=404)
    serializer = ProductSerializer(product,data=request.data,partial=True,context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({"success":True,
                         "message":f"product updated successfully",
                         "data":serializer.data},status=200)
    return Response({"success":False,
                     "message":"Product Updation Failed",
        "error":serializer.errors},status=400)

@api_view(["DELETE"])
@permission_classes([IsStaffUser])
def delete_product(request,pk):
    try:
        product=Product.objects.get(id=pk)
        product.is_available=False
        product.save()
        return Response({"success":True,
            "message":"Product Deactivated"},status=200)
    except Product.DoesNotExist:
        return Response({'success':False
            ,"message":'Product Not Found'},status=404)

@api_view(["GET"])
def get_product_by_category(request, category):
    products=Product.objects.filter(category=category,is_available=True)
    serializer = ProductSerializer(products,many=True,context={'request': request})
    return Response({'success':True,
                     "data":serializer.data},status=200)