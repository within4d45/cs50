from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post


"""
To do:
[] Catch case if requested profile user does not exist
"""


def index(request):
    if request.method == "POST":
        new_post = Post(
            content = request.POST["content"],
            user = request.user
        )
        new_post.save()
        return HttpResponseRedirect(reverse(index))

    posts = Post.objects.all().order_by("-timestamp")
    return render(request, "network/index.html", {
        "posts": posts
    })


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

def profile(request, username):
    # we do not have to catch an exception, because the user only gets to this page if
    # they click on a link
    user = User.objects.get(username = username)
    posts = Post.objects.filter(user = user.pk).order_by("-timestamp")
    follower_count = user.followers.count()
    following = False
    if user in request.user.followers.all():
        following = True
    
    return render(request, "network/profile.html", {
        "username": username,
        "follower_count":follower_count,
        "posts": posts,
        "following": following,
    })