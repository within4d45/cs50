from django.shortcuts import render
from django.http import HttpResponse

from . import util


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
