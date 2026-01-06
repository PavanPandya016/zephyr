from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import RegexValidator, MinLengthValidator
from django.core.exceptions import ValidationError


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    username = models.CharField(
        max_length=15,
        unique=True,
        db_index=True,
        null=True,       # TEMP
        blank=True,      # TEMP
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message='Username can only contain letters, numbers, and underscores'
            ),
            MinLengthValidator(3, message='Username must be at least 3 characters long')
        ]
    )

    bio = models.TextField(blank=True, max_length=160)
    avatar = models.ImageField(upload_to="avatar/", blank=True, null=True)
    banner = models.ImageField(upload_to="banner/", blank=True, null=True)

    def __str__(self):
        return f"@{self.username}"

    def clean(self):
        super().clean()
        if self.username:
            reserved_usernames = {'admin', 'root', 'api', 'settings', 'help'}
            if self.username.lower() in reserved_usernames:
                raise ValidationError({'username': 'This username is reserved'})

    def save(self, *args, **kwargs):
        if self.username:
            self.username = self.username.lower()
        self.full_clean()
        super().save(*args, **kwargs)


class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following"
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")

    def __str__(self):
        return f"{self.follower} → {self.following}"
