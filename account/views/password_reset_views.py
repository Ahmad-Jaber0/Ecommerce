from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from account.serializers.password_serializers import ResetPasswordSerializer,ForgotPasswordSerializer 
from account.utils.helpers import get_user_by_email, generate_reset_token, validate_reset_token
from account.utils.email_service import send_reset_email

@api_view(['POST'])
def forgot_password(request):
    serializer = ForgotPasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.validated_data['email']
    user = get_user_by_email(email)

    if not user or not hasattr(user, 'profile'):
        return Response({'details': 'This email is not registered or has no profile'},status=status.HTTP_400_BAD_REQUEST)

    token = generate_reset_token(user)    
    send_reset_email(user, request, token)

    return Response({'details': f'Password reset link sent to {user.email}'},status=status.HTTP_200_OK)

@api_view(['POST'])
def reset_password(request, token):
    serializer = ResetPasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = validate_reset_token(token)
    if not user:
        return Response({'error': 'Invalid or expired token'}, 
                    status=status.HTTP_400_BAD_REQUEST)

    if serializer.validated_data['password'] != serializer.validated_data['confirm_password']:
        return Response({'error': 'Passwords do not match'}, 
                    status=status.HTTP_400_BAD_REQUEST)

    user.set_password(serializer.validated_data['password'])
    user.save()
    
    user.profile.reset_password_token = None
    user.profile.reset_password_expire = None
    user.profile.save()

    return Response({'details': 'Password reset successful'}, 
                status=status.HTTP_200_OK)