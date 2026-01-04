from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from posts.models import Zeph
from .models import Like, Bookmark

@login_required
def toggle_like(request, zeph_id):
    zeph = get_object_or_404(Zeph, id=zeph_id)

    like, created = Like.objects.get_or_create(
        user = request.user,
        zeph = zeph
    ) 

    if not created:
        like.delete()

    return redirect(request.META.get("HTTP_REFERER", "posts:feed"))

@login_required
def toggle_bookmark(request, zeph_id):
    zeph = get_object_or_404(Zeph, id=zeph_id)

    bookmark, created = Bookmark.objects.get_or_create(
        user = request.user,
        zeph = zeph
    )
    if not created:
        bookmark.delete()

    return redirect(request.META.get("HTTP_REFERER", "posts"))

class BookmarkListView(LoginRequiredMixin, ListView):
    model = Bookmark
    template_name = "posts/bookmark.html"
    context_object_name = "zephs"

    def get_queryset(self):
        
        bookmarked_zephs = Zeph.objects.filter(
            bookmarks__user=self.request.user
        ).select_related(
            'author', 'author__profile'
        ).prefetch_related('likes', 'bookmarks').order_by('-created_at')
        
        return bookmarked_zephs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        
        user_liked_ids = set(
            Like.objects.filter(user=self.request.user).values_list('zeph_id', flat=True)
        )
        user_bookmarked_ids = set(
            Bookmark.objects.filter(user=self.request.user).values_list('zeph_id', flat=True)
        )
        
        
        for zeph in context['zephs']:
            zeph.is_liked_by_user = zeph.id in user_liked_ids
            zeph.is_bookmarked_by_user = zeph.id in user_bookmarked_ids
        
        return context