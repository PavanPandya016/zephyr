from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views.generic import CreateView

from .models import User, Follow
from posts.models import Zeph

User = get_user_model()

@login_required
def toggle_follow(request, user_id):
    target = get_object_or_404(User, id=user_id)

    if target == request.user:
        return HttpResponseForbidden("You Can't Follow yourself")
    
    follow, created = Follow.objects.get_or_create(
        follower = request.user,
        following = target 
    )

    if not created:
        follow.delete()

    return redirect(request.META.get("HTTP_REFERER", "posts:feed"))

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "accounts/profile.html"
    context_object_name = "profile_user"

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs["username"])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        context["zephs"] = Zeph.objects.filter(author=user)
        context["followers_count"] = user.followers.count()
        context["following_count"] = user.following.count()
        context["is_following"] = (
            self.request.user.following.filter(following = user).exists()
        )

        return context
    
class SignUpView(CreateView):
    model = User
    fields = ("username", "email", "password")
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        return super().form_valid(form)
