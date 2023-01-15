from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core import serializers

from .models import User, Post


"""
To do:
[] Catch case if requested profile user does not exist
[] Catch case the followed user doesn't exist
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

def posts(request):
    posts = request.user.posts.all()
    data = serializers.serialize("json", posts)
    return JsonResponse({
        "data": data
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

def profile(request, user_id):
    # we do not have to catch an exception, because the user only gets to this page if
    # they click on a link
    
    # create a dict with the passed variables
    variables = {}
    user = User.objects.get(pk = user_id)
    variables["profile_user"] = user
    variables["posts"] = Post.objects.filter(user = user.pk).order_by("-timestamp")
    variables["follower_count"] = user.followers.count()
    
    # Check if user is authenticated
    if request.user.is_authenticated:
        # give the option to follow or unfollow, pass these values to the view
        # and then use that information in the follow() post function
        follow_button_value = "Follow"
        followed = 0
        if user in request.user.following.all():
            follow_button_value = "Unfollow"
            followed = 1
        variables["follow_button_value"] = follow_button_value
        variables["followed"] = followed

    return render(request, "network/profile.html", variables)

def follow(request, user_id, followed):
    if request.method == "POST":
        if followed == 0:
            request.user.following.add(user_id)
        else:
            request.user.following.remove(user_id)
        return HttpResponseRedirect(reverse("profile", args=[user_id]))
    
def followed(request):
    if not request.user.is_authenticated:
        return render(request, "network/error_not_signed_in.html")
    users = request.user.following.all()
    posts = Post.objects.filter(user__in=users).order_by("-timestamp")
    return render(request, "network/index.html", {
        "heading": "These post are only posts of people that you are following",
        "posts": posts
    })