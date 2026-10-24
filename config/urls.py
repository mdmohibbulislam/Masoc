# config/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # Django tries each include in order; paths within each app are unique
    # so both can share the "accounts/" prefix without shadowing each other.
    path("accounts/", include("django.contrib.auth.urls")),   # login, logout, password reset
    path("accounts/", include("accounts.urls")),              # signup, profiles, follow, search
    path("", include("posts.urls")),                          # home feed, post detail, likes
]