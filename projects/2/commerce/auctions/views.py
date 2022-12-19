from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Auction, Bid

"""
To do:
[] Change price to current bit in index view

"""

class NewAuctionForm(forms.Form):
    title = forms.CharField(label="Auction Title", max_length=64)
    description = forms.CharField(label="Description", max_length=256)
    starting_price = forms.IntegerField(label="Starting bid")
    picture_url = forms.CharField(
        label="Picture URL (optional)", max_length=256, required=False
    )


def index(request):
    auctions = Auction.objects.all()
    return render(request, "auctions/index.html", {"auctions": auctions})


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def auction(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    return render(request, "auctions/auction.html",{
        "auction": auction, 
        "bids": auction.bids.all(),
        "comments": auction.comments.all()
    })


def new_auction(request):
    """
    To do:
    [x] Auction name check
    - Add duration and starting time
    - Work with categories
    """
    if request.method == "POST":
        form = NewAuctionForm(request.POST)

        if (
            form.is_valid()
            and not Auction.objects.filter(title=form.cleaned_data["title"]).exists()
        ):
            auction = Auction(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                picture_url=form.cleaned_data["picture_url"],
                price=form.cleaned_data["starting_price"],
                user=request.user,
            )
            auction.save()

        else:
            return render(
                request,
                "auctions/new_auction.html",
                {
                    "message": "An auction with that title already exists. please choose a different one.",
                    "form": NewAuctionForm(),
                },
            )

    return render(request, "auctions/new_auction.html", {"form": NewAuctionForm()})

def bid(request, auction_id):
    if request.method == "POST":
        # insert logic here to post a bid
        pass