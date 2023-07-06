from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entries(request, entry):
    return render (request, "encyclopedia/entry.html", {
        "title": entry,
        "description": util.get_entry( title = entry)
    })
