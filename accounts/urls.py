from django.urls import path
from django.contrib.auth import views as auth_views

from .views import toggle_follow, ProfileView, SignUpView
 
app_name = "accounts"

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("password-change/", auth_views.PasswordChangeView.as_view(
        template_name="accounts/password_change.html",
        success_url="/"
    ), name="password_change"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("folllow/<int:user_id>/", toggle_follow, name="follow"),
    path("<str:username>/", ProfileView.as_view(), name="profile"),
]