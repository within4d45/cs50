from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from . import util
from .models import User, Auction, Bid, Comment, WatchList

"""
To do:
[x] Change price to current bit in index view
[x] Have a highest bid + starting price field in Auction instead of price
[] Change bid view when there have not been any bids
[] Make watchlist items have a different bg when the auction isn't active any more
[] Change minimum bid or price when auction is created first
[] The bid logic in the auction site view is pretty weird
    [] How do you go about creating logic in a different place but sending messages over to be displayed in the rendered form?
[] fine tune error handling when auction is created
[] having the bidding logic within the auction view is probably not best practice
[] make it so the user that has created the auction must not bid
[] handle letter overflow

[-] overlooking the url logic on the other pages
[-] figure out if through that people can just insert stuff
 
Questions:
[-] If people manage to add bids without the interface, the price of the piece will not get updated
  [-] If people manage to add a bid under the current highest bid, the Bid.objects.all().last() will not give out the highest

"""

class NewAuctionForm(forms.Form):
    title = forms.CharField(label="", max_length=32, widget=forms.TextInput(attrs={'class':'form-input text', 'placeholder':'Title'}))
    description = forms.CharField(label="", max_length=256,widget=forms.Textarea(attrs={'class':'form-input textarea', 'rows':'4', 'placeholder':'Description'}))
    starting_price = forms.IntegerField(label="", widget=forms.TextInput(attrs={'class':'form-input text', 'placeholder':'Starting Price'}))
    picture_url = forms.CharField(
        label="", max_length=256, required=False, widget=forms.TextInput(attrs={'class':'form-input text', 'placeholder':'Image URL (optional)'})
    )


class NewBidForm(forms.Form):
    bid = forms.IntegerField(label="Place your bid")


class NewCommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder':"Enter comment here",
        'style':'width: 100%; height: 150px;'
    }))


def index(request):
    auctions = Auction.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "auctions": auctions,
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
            watchlist = WatchList(user=user)
            watchlist.save()
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
    any_bids = auction.bids.filter().exists()
    watchlist = request.user.watchlist
    auction_in_watchlist = watchlist.auction.filter(pk=auction.pk).exists()
    message = ""
    error = ""

    if request.method == "POST":
        form_bid = NewBidForm(request.POST)
        if form_bid.is_valid():
            bid = int(form_bid.cleaned_data['bid'])
        if bid < auction.price:
            error = "Place a bid higher than the current price"
        else:
            message = "Bid succesfully received"
            new_bid = Bid(amount=bid, auction = auction, user = request.user)
            new_bid.save()
            auction.price = bid+1
            auction.save()

        return render(request, "auctions/auction.html",{
            "auction": auction, 
            "bids": auction.bids.all(),
            "any_bids": any_bids,
            "comments": auction.comments.all(),
            "form_bid": NewBidForm(),
            "form_comment": NewCommentForm(),
            "user": request.user,
            "message": message,
            "error": error,
            "watchlist": watchlist,
            "auction_in_watchlist": auction_in_watchlist
        })

    return render(request, "auctions/auction.html",{
        "auction": auction, 
        "bids": auction.bids.all(),
        "any_bids": any_bids,
        "comments": auction.comments.all(),
        "form_bid": NewBidForm(),
        "form_comment": NewCommentForm(),
        "user": request.user,
        "watchlist": watchlist,
        "auction_in_watchlist": auction_in_watchlist
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
        if (form.is_valid() and not Auction.objects.filter(title=form.cleaned_data["title"]).exists()):
            auction = Auction(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                picture_url=form.cleaned_data["picture_url"],
                price=form.cleaned_data["starting_price"],
                user=request.user,
            )
            auction.save()

        else:
            return render(request, "auctions/new_auction.html",{
                    "message": "An auction with that title already exists. Please choose a different one.",
                    "form": NewAuctionForm(),
                })

    return render(request, "auctions/new_auction.html", {
        "form": NewAuctionForm()
        })


def watchlist(request):
    user = request.user
    auctions = user.watchlist.auction.all()
    return render(request, "auctions/watchlist.html", {
        "auctions": auctions
    })


def edit_watchlist(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    watchlist = User.objects.get(pk = request.user.pk).watchlist

    if request.method == "POST":
        if request.POST["delete"] == "True":
            watchlist.auction.remove(auction)
            watchlist.save()
        elif request.POST ["delete"] == "False":
            watchlist.auction.add(auction)
            watchlist.save
        return HttpResponseRedirect(reverse('watchlist'))


def close_auction(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    if request.method == "POST" and request.user == auction.user:
        auction.active = False
        auction.save()
    return HttpResponseRedirect(reverse('auction', args=[auction_id]))


def submit_comment(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    if request.method =="POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            new_comment = Comment(
                comment = comment,
                auction = auction,
                user = request.user
            )
            new_comment.save()
    return HttpResponseRedirect(reverse('auction', args=[auction.pk]))