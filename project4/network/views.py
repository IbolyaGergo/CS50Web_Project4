import json
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


def index(request):
    posts = Post.objects.all()
    posts = posts.order_by("-timestamp").all()

    # Show 10 posts per page
    paginator = Paginator(posts, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    title = "All Posts"
    
    return render(request, "network/index.html", {
        "posts": posts,
        "title": title,
        "page_obj": page_obj
    })

@login_required
def following(request):
    # posts = Post.objects.filter(user=request.user.following).all()
    all_posts = Post.objects.all().order_by("-timestamp").all()
    posts = []
    for post in all_posts:
        if post.user in request.user.following.all():
            posts.append(post)
    
    title = "Following"
    return render(request, "network/index.html", {
        "posts": posts,
        "title": title
    })

def new_post(request):
    if request.method == "POST":
        # Get contents of post
        body = request.POST["body"]
        post = Post(
            user=request.user,
            body=body
        )
        post.save()
        return HttpResponseRedirect(reverse("index"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
def profile(request, user_id):
    profile = User.objects.get(pk=user_id)
    
    if request.method == "GET":
        posts = Post.objects.filter(user=profile)
        posts = posts.order_by("-timestamp").all()

        return render(request, "network/profile.html", {
            "profile": profile,
            "posts": posts
        })

    if request.method == "PUT":
        if profile in request.user.following.all():
            request.user.following.remove(profile)
        else:
            request.user.following.add(profile)
        print(request.user.following.all())
        return HttpResponse(status=204)


@csrf_exempt
@login_required
def edit_post(request, post_id):
    if request.method == "PUT":
        post = Post.objects.get(pk=post_id)
        data = json.loads(request.body)
        if data.get("post_body") is not None:
            post.body = data["post_body"]
            post.save()
        return HttpResponse(status=204)

@csrf_exempt
@login_required
def like_post(request, post_id):
    if request.method == "PUT":
        post = Post.objects.get(pk=post_id)

        if request.user in post.likers.all():
            post.likers.remove(request.user)
        else:
            post.likers.add(request.user)

        return HttpResponse(status=204)
        

