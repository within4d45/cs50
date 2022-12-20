from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):  
    pass

class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    picture_url = models.CharField(max_length=256, blank = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")
    price = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} by {self.user}"

class Bid(models.Model):
    amount = models.IntegerField()
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidders")
    
    def __str__(self):
        return f"{self.amount}$"

class Comment(models.Model):
    comment = models.CharField(max_length=1028)
    auction = models.ForeignKey(Auction,on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentator")


    def __str__(self):
        return f"{self.comment}"

class WatchList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="watchlist")
    auction = models.ManyToManyField(Auction, blank=True, related_name="watchlists")

    def __str__(self):
        return f"{self.user}'s watchlist"