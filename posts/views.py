from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.models import Follow

from .forms import CommentForm, PostForm
from .models import Like, Post


def home(request):
    # visitors who are not logged in just see the welcome page
    if not request.user.is_authenticated:
        return render(request, "home.html")

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # build the Post but don't save yet
            post.author = request.user  # the form doesn't ask who wrote it
            post.save()
            return redirect("home")  # reload the page so a refresh doesn't re-post
    else:
        form = PostForm()

    # the feed: your own posts plus posts from people you follow
    following_ids = Follow.objects.filter(follower=request.user).values_list(
        "following_id", flat=True
    )
    posts = Post.objects.filter(
        Q(author=request.user) | Q(author_id__in=following_ids)
    ).select_related("author").prefetch_related("likes", "comments")

    # collect liked post IDs so the template can highlight them
    liked_ids = set(
        Like.objects.filter(user=request.user, post__in=posts).values_list(
            "post_id", flat=True
        )
    )

    return render(request, "home.html", {"form": form, "posts": posts, "liked_ids": liked_ids})


def post_detail(request, pk):
    post = get_object_or_404(Post.objects.select_related("author"), pk=pk)
    comments = post.comments.select_related("author").order_by("created_at")

    is_liked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(user=request.user, post=post).exists()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("post_detail", pk=pk)
    else:
        form = CommentForm()

    return render(request, "post_detail.html", {
        "post": post,
        "comments": comments,
        "form": form,
        "is_liked": is_liked,
        "likes_count": post.likes.count(),
    })


@login_required
@require_POST
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    # return to wherever the user came from
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "home"
    return redirect(next_url)
