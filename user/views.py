from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import AuthenticationFailed

from .models import User
from django.core.mail import send_mail
from rest_framework import status
from django.core.cache import cache
import environ
from pathlib import Path
import os
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import os


# Create your views here.
env = environ.Env(
    DEBUG=(bool, False)
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
     "models/gemini-2.0-flash-001:generateContent"
)



import json
@api_view(["POST"])
def premium_english_tutor(request):
    
    sentence = request.data.get("sentence")

    if not sentence:
        return Response(
            {"error": "Sentence is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    prompt = f"""
Return ONLY valid JSON.

Format:
{{
  "correct_sentence": "",
  "better_sentence": "",
  "mistakes": [
    {{
      "wrong_part": "",
      "correct_part": "",
      "reason": ""
    }}
  ]
}}

Sentence:
"{sentence}"
"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(
            f"{GEMINI_URL}?key={settings.GEMINI_API_KEY}",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=20
        )
    except requests.exceptions.RequestException:
        return Response(
            {"error": "Gemini service unreachable"},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    print("STATUS:", response.status_code)
    print("BODY:", response.text)

    if response.status_code != 200:
        return Response(
            {
                "error": "Gemini API failed",
                "details": response.text
            },
            status=status.HTTP_502_BAD_GATEWAY
        )

    try:
        data = response.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        ai_json = json.loads(text)
    except Exception:
        return Response(
            {"error": "Invalid Gemini response"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response({
        "input_sentence": sentence,
        **ai_json,
        "mistake_count": len(ai_json.get("mistakes", [])),
        "source": "gemini"
    })



class EnglishTutorAPIView(APIView):
    def post(self, request):
        sentence = request.data.get("sentence")

        if not sentence:
            return Response(
                {"error": "Sentence is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # LanguageTool API
        url = "https://api.languagetool.org/v2/check"
        data = {
            "text": sentence,
            "language": "en-US"
        }

        res = requests.post(url, data=data).json()
        matches = res.get("matches", [])

        mistakes = []
        corrected_sentence = sentence

        for match in matches:
            wrong_text = sentence[
                match["offset"]: match["offset"] + match["length"]
            ]

            suggestions = [r["value"] for r in match.get("replacements", [])]

            mistakes.append({
                "wrong_part": wrong_text,
                "correct_part": suggestions[0] if suggestions else "",
                "reason": match.get("message"),
                "suggestions": suggestions
            })

            if suggestions:
                corrected_sentence = corrected_sentence.replace(
                    wrong_text, suggestions[0], 1
                )

        better_sentence = corrected_sentence  # placeholder (AI later)

        return Response({
            "input_sentence": sentence,
            "mistakes": mistakes,
            "correct_sentence": corrected_sentence,
            "better_sentence": better_sentence,
            "fluency_tip": "Practice subject-verb agreement for better fluency.",
            "mistake_count": len(mistakes)
        })

# Read .env file
environ.Env.read_env(os.path.join(settings.BASE_DIR, '.env'))
@api_view(["GET"])
def get_live(request):
    return Response({"success":"Application live"})


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    MAX_ATTEMPTS=5
    BLOCK_TIME_SECONDS=600
    def get_device_key(self,request):
        print("device key called")
        ip = request.META.get('HTTP_X_FORWARDED_FOR',request.META.get("REMOTE_ADDR"))
        user_agent = request.META.get("HTTP_USER_AGENT","unknown")
        return f"login attempts:{ip}:{user_agent}"
    def validate(self,attrs):
        print("validate called")
        request=self.context.get('request')
        device_key=self.get_device_key(request)

        attempts=cache.get(device_key,0)

        if attempts>=self.MAX_ATTEMPTS:
            raise AuthenticationFailed("Too many login attempts retry after some time")
        try:
            data=super().validate(attrs)
            print("passed")
        except AuthenticationFailed as e:
            print("raised")
            cache.set(device_key,attempts+1,timeout=self.BLOCK_TIME_SECONDS)
            raise AuthenticationFailed(f"Invalid credentials ({5-(attempts+1)}) attempts remaining")
        print("proceeding")
        cache.delete(device_key)
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
    print("from",settings.EMAIL_HOST_USER)
    otp=random.randint(1111,9999)
    request.user.email_otp=otp
    request.user.email_otp_created_at=timezone.now()
    request.user.save()
    send_mail(
        subject="verify your email",
        message=f"Your OTP is {otp}",
        from_email=settings.EMAIL_HOST_USER,
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