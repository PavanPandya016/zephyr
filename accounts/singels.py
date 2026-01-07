from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import Profile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Truncate username to 15 characters if needed (Profile.username max_length)
        profile_username = instance.username[:15] if len(instance.username) > 15 else instance.username
        Profile.objects.create(user=instance, username=profile_username)