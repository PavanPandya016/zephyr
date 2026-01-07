from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.views.generic import DetailView, CreateView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, login
from django.db import transaction

from .models import Profile, Follow
from .forms import CustomUserCreationForm
from posts.models import Zeph

User = get_user_model()


@login_required
def toggle_follow(request, user_id):
    """Toggle follow status for a user."""
    if request.method != 'POST':
        return HttpResponseForbidden("Invalid request method")
    
    target = get_object_or_404(User, id=user_id)

    if target == request.user:
        return HttpResponseForbidden("You can't follow yourself")

    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target
    )

    if not created:
        follow.delete()

    return redirect(request.META.get("HTTP_REFERER", "/"))


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "accounts/profile.html"
    context_object_name = "profile_user"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_object(self):
        # Lookup by Profile.username instead of User.username
        username = self.kwargs.get(self.slug_url_kwarg)
        profile = get_object_or_404(Profile, username=username)
        return profile.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object

        context["zephs"] = Zeph.objects.filter(author=user).order_by('-created_at')
        context["followers_count"] = user.followers.count()
        context["following_count"] = user.following.count()
        context["is_following"] = (
            self.request.user.is_authenticated and
            self.request.user.following.filter(following=user).exists()
        )

        return context


class SignUpView(FormView):
    form_class = CustomUserCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:profile_setup")

    @transaction.atomic
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.request.session["signup_user_id"] = user.id

        return redirect(self.get_success_url())


class ProfileSetupView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ("bio", "avatar", "banner")
    template_name = "accounts/profile_setup.html"

    def get_object(self):
        user_id = self.request.session.get("signup_user_id")

        if not user_id:
            # If no signup_user_id, use the current logged-in user
            user = self.request.user
        else:
            user = User.objects.get(id=user_id)

        # Truncate username to 15 characters if needed (Profile.username max_length)
        profile_username = user.username[:15] if len(user.username) > 15 else user.username
        
        profile, _ = Profile.objects.get_or_create(
            user=user,
            defaults={'username': profile_username}
        )
        # Ensure username is set even if profile already exists
        if not profile.username:
            profile.username = profile_username
            profile.save()
        return profile

    def form_valid(self, form):
        response = super().form_valid(form)

        # cleanup session
        self.request.session.pop("signup_user_id", None)

        return response

    def get_success_url(self):
        return reverse_lazy(
            "accounts:profile",
            kwargs={"username": self.request.user.profile.username}
        )