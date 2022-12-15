from django.urls import path

from . import views 

urlpatterns = [
    path("", views.index, name="index"),
    path("entry/<str:entry>", views.entry, name="entry"),
<<<<<<< HEAD
    path("search", views.search, name="search")
=======
    path("seach", views.search, name="search")
>>>>>>> d3f0e5695c1f8bb74185705ed261f4a77ed1e25a
]
