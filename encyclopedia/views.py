from django.shortcuts import render

from . import util
import re


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entries(request, entry):
    description = util.convert_markdown( title = entry)
    if description is None:
        error_404 = re.compile(r"\*entry name\*")
        return render(request, 'encyclopedia/error.html', {
            "description": error_404.sub(entry, util.errors["404"])
        })
    return render (request, "encyclopedia/entry.html", {
        "title": entry,
        "description": description
    })
