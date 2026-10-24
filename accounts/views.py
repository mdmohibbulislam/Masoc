from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ProfileEditForm
from .models import Follow, Profile

User = get_user_model()


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log the new user in straight away
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


def profile_detail(request, username):
    profile_user = get_object_or_404(User, username=username)
    # get_or_create protects users who signed up before the Profile signal existed
    profile_obj, _ = Profile.objects.get_or_create(user=profile_user)

    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user, following=profile_user
        ).exists()

    posts = profile_user.posts.select_related("author")

    context = {
        "profile_user": profile_user,
        "profile": profile_obj,
        "is_following": is_following,
        "followers_count": profile_user.followers.count(),
        "following_count": profile_user.following.count(),
        "posts": posts,
    }
    return render(request, "profile_detail.html", context)


@login_required
@require_POST
def toggle_follow(request, username):
    target = get_object_or_404(User, username=username)

    if target != request.user:  # you can't follow yourself
        follow, created = Follow.objects.get_or_create(
            follower=request.user, following=target
        )
        if not created:  # already following, so this click means unfollow
            follow.delete()

    return redirect("profile", username=username)


@login_required
def edit_profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=profile_obj)
        if form.is_valid():
            form.save()
            return redirect("profile", username=request.user.username)
    else:
        form = ProfileEditForm(instance=profile_obj)
    return render(request, "edit_profile.html", {"form": form})


def user_search(request):
    query = request.GET.get("q", "").strip()
    results = []
    following_ids = set()
    if query:
        results = list(
            User.objects.filter(
                Q(username__icontains=query)
            ).exclude(pk=request.user.pk if request.user.is_authenticated else None)[:20]
        )
    if request.user.is_authenticated and results:
        following_ids = set(
            Follow.objects.filter(
                follower=request.user, following__in=results
            ).values_list("following_id", flat=True)
        )
    return render(request, "search.html", {
        "query": query,
        "results": results,
        "following_ids": following_ids,
    })