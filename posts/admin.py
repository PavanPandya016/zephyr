from django.contrib import admin
from .models import Zeph

@admin.register(Zeph)
class ZephAdmin(admin.ModelAdmin):
    list_display = ("author", "content", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("author__username", "content")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",) 

    def short_content(self, obj):
        return obj.content[:40] + "..." if len(obj.content) > 40 else obj.content

    short_content.short_description = "Content"