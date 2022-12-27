from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from . import util
from .models import User, Auction, Bid, Comment, WatchList, Category

"""
Final notes:

General:
- I did not handle letter overflow
- At some point I lost track of all the wrappers and padding and margins to keep everything in the same
  style. I think I need some training with that but it's not worth the time investment for me now to 
  redo everything. I think I can train that in future projects, too.
- Website is not, yet responsive

Category:
- the categories are not ordered alphabetically nor is "No Category" at top which would make sense
- it's only possible to bind one auction with one category at the moment
- Category views extend the index view and just filter differently
- the owner of the auction can change the category

Index / Auctions overview / Category view:
- Website is not centered, when flex items are reordering - I don't like it but i wanna do better next project

Auction:
- Auction site looks pretty bad, but I've spent so much site with the site that having the logic down is 
  enough for me and I will design nice stuff later

Bidding:
- is having the bidding logic within the auction view fine or should I outsource it to a different view 
  that is handling post requests and then coming back?
- you cannot bid as the owner of the auction

Watchlist:
- active auction appear the same as inactive / finished auctions
- watchlist.html could probably somehow extend index.html, but I couldn't figure what makes most sense

Final thoughts:
- I learned a lot and I did not know anything about designing a website when starting. That's why everything
  is so messy - but that's why I don't wanna re-do every detail but move along and do that in the next projects.

  ~~ I WOULD LOVE SOME FEEDBACK ~~
"""

class NewAuctionForm(forms.Form):
    title = forms.CharField(label="", max_length=32, widget=forms.TextInput(attrs={'class':'form-input text', 'placeholder':'Title'}))
    description = forms.CharField(label="", max_length=256,widget=forms.Textarea(attrs={'class':'form-input textarea', 'rows':'4', 'placeholder':'Description'}))
    starting_price = forms.IntegerField(label="", widget=forms.TextInput(attrs={'class':'form-input text', 'placeholder':'Starting Price'}))
    category = forms.ChoiceField(
        label="Choose Category",
        choices= Category.objects.all().values_list('pk', 'name'),
        widget=forms.Select(attrs={'class':'form-input'})
        )
    picture_url = forms.CharField(
        label="", max_length=256, required=False, widget=forms.TextInput(attrs={'class':'form-input text', 'placeholder':'Image URL (optional)'})
    )


class NewBidForm(forms.Form):
    bid = forms.IntegerField(
        label="",
        widget=forms.NumberInput(attrs={'class':'form-input'})
        )


class NewCommentForm(forms.Form):
    comment = forms.CharField(label="", max_length=256,widget=forms.Textarea(attrs={'class':'form-input textarea', 'rows':'4', 'placeholder':'Enter comment here'}))


def index(request):
    auctions = Auction.objects.filter(active=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "auctions": auctions,
        "categories": categories,
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
    categories = Category.objects.exclude(name=auction.category.name)
    message = ""
    error = ""

    if request.user.is_authenticated:
        watchlist = request.user.watchlist
        auction_in_watchlist = watchlist.auction.filter(pk=auction.pk).exists()
    
    else:
        watchlist = ""
        auction_in_watchlist = ""

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
            "auction_in_watchlist": auction_in_watchlist,
            "categories": categories
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
        "auction_in_watchlist": auction_in_watchlist,
        "categories": categories
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
        
        if not (form.is_valid()):
            return render(request, "auctions/new_auction.html",{
                "message": "Form is not valid",
                "form": NewAuctionForm(),
            })

        if Auction.objects.filter(title=form.cleaned_data["title"]).exists():
            return render(request, "auctions/new_auction.html",{
                "message": "An auction with that title already exists. Please choose a different one.",
                "form": NewAuctionForm(),
            })

        picture_url = form.cleaned_data["picture_url"]

        if picture_url == "":
            picture_url = "https://picsum.photos/id/119/300/200"

        auction = Auction(
            title=form.cleaned_data["title"],
            description=form.cleaned_data["description"],
            picture_url=picture_url,
            price=form.cleaned_data["starting_price"],
            category = Category.objects.get(pk=form.cleaned_data["category"]),
            user=request.user,
        )
        auction.save()

        return HttpResponseRedirect(reverse('auction', args=[auction.pk]))

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

def category(request):
    category_chosen=request.GET['category_chosen']
    auctions = Auction.objects.filter(active=True).filter(category = Category.objects.get(name=category_chosen))
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "auctions": auctions,
        "categories": categories,
        "chosen_category": category_chosen
        })

def change_category(request):
    if request.method=="POST":

        category_name= request.POST['category_chosen']
        auction_title= request.POST['auction']
        
        # return render(request, "auctions/test.html", {
        #   "category_name": category_name,
        #   "auction_title": auction_title  
        # })

        category = Category.objects.get(name=category_name)
        auction = Auction.objects.get(pk=auction_title)

        auction.category = category
        auction.save()

        return HttpResponseRedirect(reverse('auction', args=[auction.pk]))