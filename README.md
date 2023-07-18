# Distinctiveness and Complexity

# Technical documentation of the project
## Code specification
The definition of the initial distribution code could be found in [Project 1](https://cs50.harvard.edu/web/2020/projects/1/wiki/)description. Development changes are listed below.
### HTML templates and static files
- **Changes in HTML templates and static files**
    - *layout.html*: added action and csrf_token to search form, added links to 'Create new page' and 'Random page' in the sidebar.
    - *index.html*: added links to a list of encyclopedia entries
    - *styles.css*: changed style for `textarea` element and added styles for `toolbar, tb-item-flex, tb-item-fixed` HTML-element classes. 
- **New HTML templates**
    - *entry.html*
The new template provides information about the encyclopedia's entry. This template inherits from a base `layout.html`. Contained page title with entry name,  toolbar, and entry description. The toolbar provided information about the reading mode and the ability to go to the entry editor.
    - *search.html*
The new template provides information about the sidebar search result. This template inherits from a base `layout.html`. Provided a list of entries that partly matches the search query. A search query is a substring of an entry name.
    - *new_entry.html* 
The new template represents the form for submitting information about the new entry to the encyclopedia. This template inherits from a base `layout.html`. Contained the entry's title input field, entry's description textarea, and submit button.
    - *editor.html*
The new template represents the form for editing the encyclopedia's entry. This template inherits from a base `layout.html`. Contained the entry's description textarea and save button.
    - *error.html*
Template for the error page. This template inherits from a base `layout.html` and contains information about an error.
### Changes in __util.py__
Added global dictionary of errors texts:
```
errors = {
    "404" : f"Sorry, there is no information about <b>*1*</b> in our encyclopedia...",
    "search": f"There is no result for <b>*1*</b>. Try another keyword.",
    "empty": "You must input the search value.",
    "entryDuplication": "The entry <b>*1*</b> is already in our encyclopedia. You cannot add existing items. However you could <a href='/wiki/edit/*1*'>change</a> it."
}
```
Added function `convert_markdown(title)`, which takes entry title, searches entry in encyclopedia by it, if there is requested entry, return converted to HTML description of the entry. To convert the description from Markdown to Html `markdown2` library is imported and `markdown2.markdown()` is used.
Added function `list_entries_with_parameter(search_entry)`. It returns the list of entries whose title includes `search_entry` as a substring.
### Changes in __urls.py__
Added new paths:
```
    path("wiki/<str:entry>", views.entries, name="entry" ),
    path("search", views.search, name="search"),
    path("new_entry", views.addEntry, name="new_entry"),
    path("wiki/edit/<str:entry>", views.changeEntry, name="editor" ),
    path("random", views.randomEntry, name="random")
```
- *entry* path - related to the entry page
- *search* path related to the search page
- *new_entry* path related to *Create New Page* link
- *editor* path related to the *Edit* link on entry page
- *random* path related to the *Random Page* link
### Changes in __views.py__
Added `entries(request, entry)` view to represent the entry page. Firstly, the system tried to take converted to an HTML description of the entry by its title. If the description is None then the system renders the error page with the error `"404"`, else system renders to entry's page with initialized *title* and *description*
Added `search(request)` view to represent the result of the sidebar search.
There are two options in this view
1. `request.method` is **POST**
The system checked if the post request included only an empty string and then rendered the error page with the error key `"empty"`.
Else system gets the list of entries that contains post request as a substring of their title
`entries = util.list_entries_with_parameter(search_entry)`
If there are no entries in the encyclopedia that are contained in their title post request a substring system renders the error page with the error key `"search"`.
If there is 1 entry in the encyclopedia whose title is exactly the same as the post request then the system redirects to the entry page.
If there is more than 1 coincidence or only one but the post request is only a substring of the entry title then the system renders a search page with the list of suitable entries.
2. `request.method` is **GET**
The system redirects to the index page.

Added class `EntryForm(forms.Form)` that contained 2 `CharFields`:
1. **title** - it is TextInput with attributes `{'name':'title', 'label':'Title'}`
2. **description** - it is Textarea with attributes `{'name':'description', 'label':'Entity description', 'placeholder' : 'Describe new entity with all opportunities of Markdown format'}`

Added `addEntry(request)` view to represent an ability to create a new entry in the encyclopedia.
There are two options in this view
1. `request.method` is **POST**
The system checked if the form sent by post request is valid.
If the form is valid then the system checked if the entry is unique in the encyclopedia.
If there is a new entry then the system saves it and redirects to a new entry's page. 
The system renders the error page if an entry with the same title already exists in the encyclopedia with the error key `"entryDuplication"`
If the form is not valid then the system renders the new_entry.html with the same object of `EntryForm` class
2. `request.method` is **GET**
The system renders the new_entry.html with a new object of `EntryForm` class

Added `changeEntry(request, entry)` view to represent the ability to change existing entries.
There are two options in this view
1. `request.method` is **POST**
The system checked if the form sent by post request is valid.
If the form is valid, the system checked that entry provided by post request exists in the encyclopedia. If there is such an entry system saves changes and redirects to the entry's page. If there is no such entry then the system shows the error page with the error key `"404"`.
If the form is not valid then the system renders the new_entry.html with the same object of `EntryForm` class and title
2. `request.method` is **GET**
The system tries to get the description for the provided title. If there is no such entry in the encyclopedia, the system shows an error page with the error key `"404"`. If the requested item exists, the system renders `editor.html` page with provided information for the title of the entry and form as a new `EntryForm` object with a predefined *title* and *description* field:
```
return render(request, "encyclopedia/editor.html", {
        "title": entry,
        "form": EntryForm(initial={'description': description,
                                   'title': entry})
```
Added `randomEntry(request)` view to represent a random entry page from the encyclopedia. The system gets the list of all entries. Then using the included `random` library take a random title from that list:
```entryTitle = entryList[random.randint(0, len(entryList))-1]```
In the end, the system redirects to the enrty.html page with chosen entry title.

## Installation
To install the current project locally user should download the whole code from the current repository, then in the terminal run a command:
```python manage.py  runserver```. After that action user could find the server path in `Starting development server at <<provided path>>` line. Then the user may click, copy or text this `<<provided path>>` in a browser.
## User guide
On the initial page of the encyclopedia, the user could see the list of all pages in the encyclopedia. The user is able to look at any entry by clicking the link from the main page. On the entry page user sees the title and description of the entry and the current page mode. By default, the user is in the *Read* mode of the page. It is possible to change encyclopedia article information by clicking the **_Edit_** link in the page toolbar.
When the user clicks **_Edit_** the editor is opened. The user sees the description of the editable entry and could add any type of information in Markdown syntax. After editing, the user should click the **Save** button.
The user is able to search any encyclopedia entry by using a sidebar search box. From any page of the encyclopedia user could text request into the search box and press `Enter`.
If there is one exactly the same as the requested entry in the encyclopedia - the user would be redirected to it. If there is more than one entry that title includes as a substring of the user's query then the user would see the search page with the list of results.
The user is able to create a new entry by clicking the **_Create new Page_** link. After clicking, the user would be redirected to a new page editor. The user should provide the title of the new entry and the description. The description should be provided with Markdown syntax.
After submitting information to the encyclopedia user could see 2 different pages. If users successfully submit a new entry, the entry page would be opened. If the user submits information about an already existing entry (the title is exactly the same), the error page would be opened with a proposal to edit the existing page instead of adding a duplicate entry.
There is one more option in the encyclopedia. Users could open a random page by clicking **_Random Page_** in the sidebar from any page of the encyclopedia.



