from django.shortcuts import render, redirect

from . import util
import re
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entries(request, entry):
    description = util.convert_markdown( title = entry)
    if description is None:
        '''
        If there is no information about requested entry, show the error
        '''
        error_descr = re.compile(r"\*1\*")
        return render(request, 'encyclopedia/error.html', {
            "description": error_descr.sub(entry, util.errors["404"])
        })
    return render (request, "encyclopedia/entry.html", {
        "title": entry,
        "description": description
    })

def search(request):
    if request.method == "POST":
        search_entry = request.POST['q']
        if search_entry != "":
            '''
            Try to get list of entries that contain search entry
            '''
            entries = util.list_entries_with_parameter(search_entry) 
            if len(entries) == 0:
                '''
                If there is no result, show the search error information
                '''
                error_descr = re.compile(r"\*1\*")
                return render(request, 'encyclopedia/error.html', {
                    "description": error_descr.sub(search_entry, util.errors["search"])
                })  
            elif len(entries) == 1 and entries[0].casefold() == search_entry.casefold() :
                '''
                If there is only 1 result and search entry is exactly the same as 
                entry name in encyclopedia then open entry page
                '''
                return redirect (f"wiki/{entries[0]}", entry= entries[0] )
            else:
                '''
                If there are more than one results or search entry is only the part
                of entry name in encyclopedia, show the list of results
                '''
                return render(request, "encyclopedia/search.html", {
                            "entries": entries
                        })
        else:
            '''
            If there is an error in search form, show validation check result
            '''
            return render(request, 'encyclopedia/error.html', {
                "description": util.errors["empty"]
               })
    '''
    If the request method is get, redirect to index page
    '''
    return redirect("index")