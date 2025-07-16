from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from django.core.mail import send_mail
from rest_framework import status
# Create your views here.

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self,attrs):
        data=super().validate(attrs)
        data['role']=self.user.role
        return data
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class=CustomTokenObtainPairSerializer
@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    return Response({
        "username":request.user.username,
        "email":request.user.email,
        "role":request.user.role,
        "is_email_verified":request.user.is_email_verified
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def hello_world(request):
    return Response({"message ":"api called"})

from django.contrib.auth.password_validation import validate_password
class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(default="customer")
    class Meta:
        model= User
        fields='__all__'
    def validate_password(self, value):
        validate_password(value)
        return value
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

@api_view(['POST'])
def create_user(request):
    data=request.data.copy()
    data['role']='customer'
    serializer=UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":f"User {serializer.validated_data['username']} created"})
    else:
        print(serializer.errors)
        return Response({"message":serializer.errors})
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_drivers_list(request):
    drivers=User.objects.filter(role="delivery")
    serializer=UserSerializer(drivers,many=True)
    return Response(serializer.data)

import random
from django.utils import timezone
from datetime import timedelta
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_email_otp(request):
    print(request.user)
    otp=random.randint(1111,9999)
    request.user.email_otp=otp
    request.user.email_otp_created_at=timezone.now()
    request.user.save()
    send_mail(
        subject="verify your email",
        message=f"Your OTP is {otp}",
        from_email="smarthomesystem515",
        recipient_list=[request.user.email],
        fail_silently=False
    )
    return Response({"message":"Done"})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def verify_email_otp(request):
    user=request.user
    otp_input=request.data.get("otp")

    if not otp_input:
        return Response({"error":"otp input required"})
    
    if str(user.email_otp)!=otp_input:
        return Response({"error":"Invalid Otp"})
    
    time_diff = timezone.now()-user.email_otp_created_at
    if time_diff>timedelta(minutes=2):
        return Response({"error":"Otp  has expired"})
    
    user.is_email_verified=True
    user.email_otp=None
    user.email_otp_created_at=None
    user.save()

    return Response({"message":"Email verified Successfully."})