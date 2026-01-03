from django.urls import path
from .views import toggle_bookmark, toggle_like, BookmarkListView

app_name = "engagements"

urlpatterns = [
        path("like/<int:zeph_id>/", toggle_like, name="like"),
        path("bookmark/<int:zeph_id>", toggle_bookmark, name="bookmark"),
]