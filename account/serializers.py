from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

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
        fields = ('first_name','last_name', 'email', 'username') 