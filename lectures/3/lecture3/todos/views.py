from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

class NewTaskForm(forms.Form):
    todo = forms.CharField(label="New todo")
#    priority = forms.IntegerField(label="Priority", min_value=1, max_value=5)

# Create your views here.
def index(request):
    if "todos" not in request.session:
        request.session["todos"] = []
    return render(request, "todos/index.html", {
        "todos": request.session["todos"]
    })

def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            todo = form.cleaned_data["todo"]
            request.session["todos"] += [todo]
            return HttpResponseRedirect(reverse("todos:index"))
        else:
            return render(request, "todos/add.html", {
                "form": form
            })

    return render(request, "todos/add.html", {
        "form": NewTaskForm()
    })