from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entries(request, entry):
    description = util.convert_markdown( title = entry)
    if description is None:
        return render(request, 'encyclopedia/error.html', {
            "description": f"Sorry, there is no information about <b>{entry}</b> in our encyclopedia..."
        })
    return render (request, "encyclopedia/entry.html", {
        "title": entry,
        "description": description
    })
