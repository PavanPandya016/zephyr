from django.db import models
from django.conf import settings
from posts.models import Zeph

class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    zeph = models.ForeignKey(
        Zeph,
        on_delete=models.CASCADE,
        related_name="likes",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "zeph")

class Bookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    zeph = models.ForeignKey(
        Zeph,
        on_delete=models.CASCADE, 
        related_name="bookmarks"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "zeph")

class ZephView(models.Model):
    zeph = models.ForeignKey(
        Zeph,
        on_delete=models.CASCADE,
        related_name="views"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: 
        unique_together = ("zeph", "user", "ip_address")