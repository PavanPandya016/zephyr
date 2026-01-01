from django.urls import path
from .views import (
    ZephCreateView,
    ZephDetailView,
    ZephDeleteView,
    ZephListView,
    ZephUpdateView,
    reply_zeph,
    )

app_name = "posts"

urlpatterns = [
    path("", ZephListView.as_view(), name="feed"),
    path("new/", ZephCreateView.as_view(), name="create"),
    path("<int:pk>/", ZephDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", ZephUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", ZephDeleteView.as_view(), name="delete"),
    path("<int:zeph_id>/reply/", reply_zeph, name="reply"),
]