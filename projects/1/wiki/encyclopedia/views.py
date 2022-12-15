from django.shortcuts import render
from django.http import HttpResponse
from django import forms

from . import util

<<<<<<< HEAD
class NewSearchForm(forms.Form):
    entry = forms.CharField(label="Search Encyclopedia")
=======
class SearchForm(forms.Form):
    entry = forms.CharField()
>>>>>>> d3f0e5695c1f8bb74185705ed261f4a77ed1e25a

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    if util.get_entry(entry) != None:
        return render(request, "encyclopedia/entry.html", {
            "entry_name": entry
        })
    else:
        return render(request, "encyclopedia/not_found.html",{
            "entry_name": entry
        })

def search(request):
<<<<<<< HEAD
    return render(request, "encyclopedia/search.html", {
        "search_item": request.POST("q")
=======
    query = request.POST['q']
    return render(request, "encyclopedia/search.html", {
        "query": query
>>>>>>> d3f0e5695c1f8bb74185705ed261f4a77ed1e25a
    })