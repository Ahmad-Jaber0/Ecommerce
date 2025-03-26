from datetime import timedelta
import secrets
from django.shortcuts import render

from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializers import ForgotPasswordSerializer, ResetPasswordSerializer, SignUpSerializer,UserSerializer
from rest_framework.permissions import IsAuthenticated
import hashlib
from django.utils import timezone
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.timezone import now



@api_view(['POST'])
def register(request):
    serializer = SignUpSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'تم تسجيل الحساب بنجاح!'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = UserSerializer(request.user, many=False)
    return Response(user.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=400)

def get_user_by_email(email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None

def generate_reset_token(user):
    raw_token = secrets.token_hex(16) 
    hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()  

    user.profile.reset_password_token = hashed_token
    user.profile.reset_password_expire = timezone.now() + timedelta(minutes=30)
    user.profile.save()

    return raw_token 

def send_reset_email(user, request, raw_token):
    host = request.build_absolute_uri('/')
    reset_link = f"{host}api/reset_password/{raw_token}" 
    email_body = f"Your password reset link is: {reset_link}"

    send_mail(subject="Password Reset Request",message=email_body,from_email="Ahmad@emarket.com",recipient_list=[user.email],fail_silently=False)

@api_view(['POST'])
def forgot_password(request):
    try:
        serializer = ForgotPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        user = get_user_by_email(email)

        if not user:
            return Response({'details': 'This email is not registered'}, status=status.HTTP_400_BAD_REQUEST)

        raw_token = generate_reset_token(user) 
        send_reset_email(user, request, raw_token) 

        return Response({'details': f'Password reset link sent to {user.email}'})

    except Exception:
        return Response({'details': 'An error occurred, please try again later'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def reset_password(request, token):
    try:
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        hashed_token = hashlib.sha256(token.encode()).hexdigest()
        
        user = User.objects.filter(profile__reset_password_token=hashed_token).first()
        if not user:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

        if user.profile.reset_password_expire and user.profile.reset_password_expire < timezone.now():
            return Response({'error': 'Token has expired'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['password'])
        user.profile.reset_password_token = None
        user.profile.reset_password_expire = None
        
        user.profile.save(update_fields=['reset_password_token', 'reset_password_expire'])
        user.save(update_fields=['password'])

        return Response({'details': 'Password reset successful'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': 'An error occurred, please try again later'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)