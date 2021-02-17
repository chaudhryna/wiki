import markdown2
import random
from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.contrib import messages
from . import util


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_detail(request, title):
    content = markdown2.markdown(util.get_entry(title))
    request.session['title'] = title
    return render(request, "encyclopedia/entry_detail.html", {
        "content": content
    })


def edit_entry(request):
    title = request.session.get('title')
    content = util.get_entry(title)
    form = NewEntryForm({'title': title, 'content': content})

    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)

            content = markdown2.markdown(util.get_entry(title))

            return render(request, "encyclopedia/entry_detail.html", {
                "content": content
            })

    return render(request, "encyclopedia/new.html", {
        "form": NewEntryForm({'title': title, 'content': content})
    })


def new_page(request):
    if request.method == "POST":

        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            entries = util.list_entries()
            if title in entries:
                messages.error(
                    request, "This title already exists. Please enter another.")

            else:
                util.save_entry(title, content)

                content = markdown2.markdown(util.get_entry(title))

                return render(request, "encyclopedia/entry_detail.html", {
                    "content": content
                })

    return render(request, "encyclopedia/new.html", {
        "form": NewEntryForm()
    })


def random_entry(request):
    entries = util.list_entries()
    title = random.choice(entries)

    content = markdown2.markdown(util.get_entry(title))
    return render(request, "encyclopedia/entry_detail.html", {
        "content": content
    })


def search(request):
    if request.method == 'GET':
        query = request.GET['q']
        entries = util.list_entries()

        if query in entries:

            content = markdown2.markdown(util.get_entry(query))
            return render(request, "encyclopedia/entry_detail.html", {
                "content": content
            })

        elif [match for match in entries if query in match]:

            entries = [match for match in entries if query in match]

            return render(request, "encyclopedia/index.html", {
                "entries": entries
            })

        else:

            return render(request, "encyclopedia/404.html")
