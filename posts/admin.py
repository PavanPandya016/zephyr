from django.contrib import admin
from .models import Zeph
from engagements.models import Bookmark



class CommentInline(admin.TabularInline):
    model = Zeph
    fk_name = "parent"
    extra = 0
    verbose_name = "Comment"
    verbose_name_plural = "Comments"
    readonly_fields = ("author", "created_at", "updated_at")
    fields = ("author", "content", "created_at")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(parent__isnull=False)



class BookmarkInline(admin.TabularInline):
    model = Bookmark
    extra = 0
    readonly_fields = ("user", "created_at")


@admin.register(Zeph)
class ZephAdmin(admin.ModelAdmin):
    list_display = ("author", "short_content", "created_at")
    list_filter = ("created_at",)
    search_fields = ("author__username", "content")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)

    inlines = [CommentInline, BookmarkInline]

    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(parent__isnull=True)

    def short_content(self, obj):
        return obj.content[:40] + "..." if len(obj.content) > 40 else obj.content

    short_content.short_description = "Content"
