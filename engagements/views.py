from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

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
    
 