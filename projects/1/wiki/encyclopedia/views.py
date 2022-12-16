from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
from markdown2 import Markdown

from . import util

class SearchForm(forms.Form):
    entry = forms.CharField()

markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    if util.get_entry(entry) != None:
        return render(request, "encyclopedia/entry.html", {
            "entry_name": entry,
            "content": markdowner.convert(util.get_entry(entry))
        })
    else:
        return render(request, "encyclopedia/not_found.html",{
            "entry_name": entry
        })

def search(request):
    query = request.GET['q']
    entries = util.list_entries()
    if query in entries:
        return HttpResponseRedirect(reverse("entry", args=[query]))
    else:
        results = list(filter(lambda entry: query in entry, entries))
        if len(results) == 0:
            return render(request, "encyclopedia/not_found.html",{
                "entry_name": query
        })
        else:
            return render(request, "encyclopedia/search.html", {
                "results": results
            })
    


def add(request):
    return render(request, "encyclopedia/add.html")