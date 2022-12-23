from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auction/<int:auction_id>", views.auction, name="auction"),
    path("new_auction", views.new_auction, name="new_auction"),
    path("auction/<int:auction_id>/close_auction", views.close_auction, name="close_auction"),
    path("auction/<int:auction_id>/submit_comment", views.submit_comment, name="submit_comment"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("watchlist/edit_watchlist/<int:auction_id>", views.edit_watchlist, name="edit_watchlist"),
    path("my_layout", views.my_layout, name="my_layout")
]
