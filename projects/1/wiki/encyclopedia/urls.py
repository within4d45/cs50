from django.urls import path

from . import views 

urlpatterns = [
    path("", views.index, name="index"),
    path("entry/<str:entry>", views.entry, name="entry"),
    path("seach", views.search, name="search")
]