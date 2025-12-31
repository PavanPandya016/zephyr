from django.db import models
from django.conf import settings
# Create your models here.

class Zeph(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="zephs"
    )
    content = models.TextField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author}: {self.content[:30]}"
