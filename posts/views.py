

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from .models import Zeph
from engagements.models import ZephView, Like, Bookmark
from engagements.utils import get_client_ip


class ZephListView(LoginRequiredMixin, ListView):
    model = Zeph
    template_name = "posts/feed.html"
    context_object_name = "zephs"

    def get_queryset(self):
        return (
            Zeph.objects
            .filter(parent__isnull=True)
            .select_related("author", "author__profile")
            .prefetch_related("likes", "bookmarks")
            .annotate(
                comment_count=Count("replies", distinct=True),
                view_count=Count("views", distinct=True),
            )
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_liked_ids = set(
            Like.objects.filter(user=self.request.user)
            .values_list("zeph_id", flat=True)
        )
        user_bookmarked_ids = set(
            Bookmark.objects.filter(user=self.request.user)
            .values_list("zeph_id", flat=True)
        )

        for zeph in context["zephs"]:
            zeph.is_liked_by_user = zeph.id in user_liked_ids
            zeph.is_bookmarked_by_user = zeph.id in user_bookmarked_ids

        return context


class ZephDetailView(LoginRequiredMixin, DetailView):
    model = Zeph
    template_name = "posts/detail.html"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        zeph = self.get_object()
        ip = get_client_ip(request)

        ZephView.objects.get_or_create(
            zeph=zeph,
            user=request.user,
            ip_address=ip
        )

        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        zeph = self.get_object()
        
        
        context['is_liked_by_user'] = Like.objects.filter(
            user=self.request.user, zeph=zeph
        ).exists()
        context['is_bookmarked_by_user'] = Bookmark.objects.filter(
            user=self.request.user, zeph=zeph
        ).exists()
        
        return context


class ZephCreateView(LoginRequiredMixin, CreateView):
    model = Zeph
    fields = ["content", "image"]
    template_name = "posts/create.html"
    success_url = reverse_lazy("posts:feed")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class ZephUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Zeph
    fields = ["content", "image"]
    template_name = "posts/edit.html"
    success_url = reverse_lazy("posts:feed")

    def test_func(self):
        return self.get_object().author == self.request.user
    

class ZephDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Zeph
    template_name = "posts/delete.html"
    success_url = reverse_lazy("posts:feed")

    def test_func(self):
        return self.get_object().author == self.request.user
    
def reply_zeph(request, zeph_id):
    parent = get_object_or_404(Zeph, id=zeph_id, parent__isnull=True)
    content = request.POST.get("content", "").strip()

    if content:
        Zeph.objects.create(
            author=request.user,
            content=content,
            parent=parent
        )

    return redirect("posts:detail", pk=parent.id)