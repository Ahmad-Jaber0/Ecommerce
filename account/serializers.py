from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password','username')

    
    def validate_username(self, value):
        value = value.strip()
        
        if len(value) < 4 or len(value) > 20:
            raise serializers.ValidationError("يجب أن يكون اسم المستخدم بين 4 و20 حرفًا.")
        
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError("يسمح فقط بالأحرف الإنجليزية، الأرقام، والرمز _.")
        
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("اسم المستخدم محجوز مسبقًا.")
            
        return value.lower()

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("البريد الإلكتروني غير صالح.")

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("البريد الإلكتروني مستخدم بالفعل.")

        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("يجب أن تكون كلمة المرور على الأقل 8 أحرف.")

        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("يجب أن تحتوي كلمة المرور على حرف كبير واحد على الأقل.")

        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("يجب أن تحتوي كلمة المرور على حرف صغير واحد على الأقل.")

        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("يجب أن تحتوي كلمة المرور على رقم واحد على الأقل.")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("يجب أن تحتوي كلمة المرور على رمز خاص واحد على الأقل.")

        return value

    def validate_first_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("الاسم الأول لا يمكن أن يكون فارغًا.")
        if not value.isalpha():
            raise serializers.ValidationError("الاسم الأول يجب أن يحتوي على حروف فقط.")
        return value

    def validate_last_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("الاسم الأخير لا يمكن أن يكون فارغًا.")
        if not value.isalpha():
            raise serializers.ValidationError("الاسم الأخير يجب أن يحتوي على حروف فقط.")
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance
    
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"error": "Passwords do not match"})
        return data