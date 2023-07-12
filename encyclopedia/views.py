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


class EntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'name':'title', 'label':'Title'}))
    description =  forms.CharField(widget=forms.Textarea(attrs={'name':'description', 'label':'Entity description', 'placeholder' : 'Describe new entity with all opportunities of Markdown format'}))

'''
View for creation a new entry in encyclopedia
'''
def addEntry(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            entryTitle = form.cleaned_data['title']
            if util.get_entry( entryTitle )  is None:
                util.save_entry(title=entryTitle, content = form.cleaned_data['description'] )
            else:
                '''
                If entry already exist in encyclopedia
                '''
                error_descr = re.compile(r"\*1\*")
                return render(request, 'encyclopedia/error.html', {
                    "description": error_descr.sub(entryTitle, util.errors["entryDuplication"])
                })    
        else:
            print("something go wrong")
            return render(request, "encyclopedia/new_entry.html", {
                "form": form
            })
    return render(request, "encyclopedia/new_entry.html", {
        "form": EntryForm()
    })

'''
Define the view for changing existing entries
'''
def change_entry(request, entry):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            entryTitle = form.cleaned_data['title']
            if util.get_entry( entryTitle ) is not None:
                util.save_entry(title=entryTitle, content = form.cleaned_data['description'])
                return redirect (f"/wiki/{entryTitle}", entry= entryTitle)
            else:
                '''
                If there is no information about requested entry, show the error
                '''
                error_descr = re.compile(r"\*1\*")
                return render(request, 'encyclopedia/error.html', {
                                "description": error_descr.sub(entryTitle, util.errors["404"])
                        })   
        else:
            return render(request, "encyclopedia/editor.html", {
                "title": entry,
                "form": form
            })
    description = util.get_entry( title = entry)
    if description is None:
        '''
        If there is no information about requested entry, show the error
        '''
        error_descr = re.compile(r"\*1\*")
        return render(request, 'encyclopedia/error.html', {
            "description": error_descr.sub(entry, util.errors["404"])
        })
    return render(request, "encyclopedia/editor.html", {
        "title": entry,
        "form": EntryForm(initial={'description': description,
                                   'title': entry})
    })