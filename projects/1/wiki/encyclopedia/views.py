from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
from markdown2 import Markdown
import random

from . import util

class SearchForm(forms.Form):
    entry = forms.CharField()

markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if util.get_entry(title) != None:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdowner.convert(util.get_entry(title))
        })
    else:
        return render(request, "encyclopedia/not_found.html",{
            "title": title
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

    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']

        if title in util.list_entries(): 
            return render(request, "encyclopedia/add.html", {
                "title": title,
                "content": content,
                "error": "This entry already exists, edit the existing entry or create change the title."
            })

        elif title == "" or content == "":
            return render(request, "encyclopedia/add.html", {
                "title": title,
                "content": content,
                "error": "Title and content field have to be filled."
            })
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('entry', args=[title]))
        
    else:
        return render(request, "encyclopedia/add.html", {
            "title": "",
            "content": "",
            "error": ""
        })

def edit(request, title):

    if request.method == "POST":
        content = request.POST['content']
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse('entry', args=[title]))

    else:
        content = util.get_entry(title)
        if content != None:
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "content": content
            })

        else:
            return render(request, "encyclopedia/not_found.html",{
                "title": title
            })

def random_entry(request):
    return entry(request,random.choice(util.list_entries()))