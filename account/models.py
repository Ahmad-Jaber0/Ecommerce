import hashlib
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    reset_password_token = models.CharField(max_length=64, blank=True, null=True)
    reset_password_expire = models.DateTimeField(blank=True, null=True)

    def generate_reset_token(self):
        token = str(uuid.uuid4())  
        hashed_token = hashlib.sha256(token.encode()).hexdigest() 
        self.reset_password_token = hashed_token
        self.reset_password_expire = timezone.now() + timezone.timedelta(minutes=30)
        self.save()
        return token

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
