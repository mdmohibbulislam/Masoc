from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("u/<str:username>/", views.profile_detail, name="profile"),
    path("u/<str:username>/follow/", views.toggle_follow, name="toggle_follow"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("search/", views.user_search, name="user_search"),
]