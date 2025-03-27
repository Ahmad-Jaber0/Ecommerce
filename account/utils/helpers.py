import hashlib
import secrets
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User

def get_user_by_email(email):
    return User.objects.filter(email=email).first()

def generate_reset_token(user):
    raw_token = secrets.token_hex(16) 
    hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()  

    user.profile.reset_password_token = hashed_token
    user.profile.reset_password_expire = timezone.now() + timedelta(minutes=30)
    user.profile.save()

    return raw_token 

def validate_reset_token(token):
    try:
        hashed_token = hashlib.sha256(token.encode()).hexdigest()
        user = User.objects.filter(profile__reset_password_token=hashed_token).first()
        
        if user and user.profile.reset_password_expire and user.profile.reset_password_expire > timezone.now():
            return user
        return None
    except:
        return None