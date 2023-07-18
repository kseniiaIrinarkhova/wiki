p#Distinctiveness and Complexity

#Technical documentation of project
##Code specification
Definition of initial distribution code could be found in [Project 1](https://cs50.harvard.edu/web/2020/projects/1/wiki/)description. Development changes are listed below.
###HTML templates and static files
-**Changes in HTML templates and static files**
--*layout.html*: added action and csrf_token to search form, added links to 'Create new page' and 'Random page' in sidebar.
--*index.html*: added links to list of encyclopedia entries
--*styles.css*: changed style for `textarea` element and added slyles for `toolbar, tb-item-flex, tb-item-fixed` html-element classes. 
-**New HTML templates**
--*entry.html*
New template that provide information about encyclopedia entry. This template inherits from a base `layout.html`. Contained page title with entry name,  toolbar, and entry description. Toolbar provided information about reading mode and ability to go to the entry editor.
--*search.html*
New template that provide information about sidebar search result. This template inherits from a base `layout.html`. Provided list of entries that partly matches to the search query. Search query is a substring of entry name.
--*new_entry.html* 
New template that represents the form for submitting information about new entry to encyclopedia. This template inherits from a base `layout.html`. Contened entry's title input field, entry's description textarea and submit button.
--*editor.html*
New template that represents the form for editing encyclopedia entry. This template inherits from a base `layout.html`. Contened  entry's description textarea and save button.
--*error.html*
Template for error page. This template inherits from a base `layout.html` and conteined information about an error.
###Changes in __util.py__
Added global dictionary of errors' texts *n* is template for dynamic data:
```
errors = {
    "404" : f"Sorry, there is no information about <b>*1*</b> in our encyclopedia...",
    "search": f"There is no result for <b>*1*</b>. Try another keywords.",
    "empty": "You must input the search value.",
    "entryDuplication": "The entry <b>*1*</b> is already in our encyclopedia. You cannot add existing item. However you could <a href='/wiki/edit/*1*'>change</a> it."
}
```
Added function `convert_markdown(title)`, which takes entry title, searches entry in encyclopedia by it, if there is requested entry, return converted to html description od entry. To convert description from Markdown to Html `markdown2` library is imported and `markdown2.markdown()` is used.
Added function `list_entries_with_parameter(search_entry)`. It returns the list of entries which title includes `search_entry` as a substring.
###Changes in __urls.py__
Added new paths:
```
    path("wiki/<str:entry>", views.entries, name="entry" ),
    path("search", views.search, name="search"),
    path("new_entry", views.addEntry, name="new_entry"),
    path("wiki/edit/<str:entry>", views.changeEntry, name="editor" ),
    path("random", views.randomEntry, name="random")
```
*entry* path - related to the entry page
*search* path related to the search page
*new_entry* path related to *Create New Page* link
*editor* path related to the *Edit* link on entry page
*random* path related to the *Random Page* link
###Changes in __views.py__
Added `entries(request, entry)` view to represent entry page. Firstly, system tried to take converted to HTML description of the entry by it's title. If the description is None  then system render to error page with the error  `"404"`, else system render to enrty's page with initiolized *title* and *description*
Added `search(request)` view to represent the result of sidebar search.
There are two options in this view
1. `request.method` is **POST**
System checked if the post request included only empty string then render to the error page with error key `"empty"`.
Else system gets the list of entries that containes post request as a substring of their title
`entries = util.list_entries_with_parameter(search_entry)`
If there is no entries in encyclopedia that counained in their title post request as a substring system renders to the error page with error key `"search"`.
If there is 1 enrty in encyclopedia which title exact the same as post request then system redirects to entry page.
If there is more than 1 coiniedence or only one but post request is on ly substring of entry title then system renders to search page with the list of suitable entries.
2. `request.method` is **GET**
System redirects to the index page.

Added class `EntryForm(forms.Form)` that contained 2 `CharFields`:
1. **title** - it is TextInput with attributes `{'name':'title', 'label':'Title'}`
2. **description** - it is Textarea with attributes `{'name':'description', 'label':'Entity description', 'placeholder' : 'Describe new entity with all opportunities of Markdown format'}`

Added `addEntry(request)` view to represent ability to create a new entry in encyclopedia.
There are two options in this view
1. `request.method` is **POST**
System checked if form that sended by post request is valid.
If form is valid then system checked if the entry is unique in encyclopedia.
If there is a new entry then system save it.
System renders to the error page if entry with the same title is already exist in encyclopedia with error key `"entryDuplication"`
If form is not valid then system renders to the new_entry.html with the same object of `EntryForm` class
2. `request.method` is **GET**
System renders to the new_entry.html with new object of `EntryForm` class

Added `changeEntry(request, entry)` view to represent ability of changing existin entry.
There are two options in this view
1. `request.method` is **POST**
System checked if form that sended by post request is valid.
If form is valid, system checked that entry provided by post request exists in encyclopedia. If there is such entry system saves changes and redirects to entry's page. If there is no such entry then system shows the error page with error key `"404"`.
If form is not valid then system renders to the new_entry.html with the same object of `EntryForm` class and title
2. `request.method` is **GET**
System tries to get description for provided title. If there is no such entry in encyclopedia, system shows error page with error key `"404"`. If there is requested for eddition entry, system renders to `editor.html` page with provided information for title of entry and form as new `EntryForm` object with predefined *title* and *description* field:
```
return render(request, "encyclopedia/editor.html", {
        "title": entry,
        "form": EntryForm(initial={'description': description,
                                   'title': entry})
```
Added `randomEntry(request)` view to represent random entry page from encyclopedia. System gets the list of all entries. Then using the included `random` library take random title from that list:
```entryTitle = entryList[random.randint(0, len(entryList))-1]```
At the end system redirects to the enrty.html page by chosen entry title.

##Installation
To install current project locally user should download the whole code from current repository, then in terminal run a command:
```python manage.py  runserver```. After that action user could find server path in `Starting development server at <<provided path>>` line. Then user may click, copy or text in browser this `<<provided path>>`.
##User guide
On the initial page of the encyclopedia user could see the list of all pages in the encyclopedia. User is able to look at any entry by clicking the link from the main page. On entry page user sees the title and description of entry and current page mode. By default user in *Read* mode of the page. It is possible to change information of encyclopedia article by clicking **_Edit_** link in page toolbar.
When user clicks **_Edit_** the editor is opened. User sees the description of editable enty and could add any type of information in Markdown syntax. After editing, user should click **Save** button.
User is able to search an any encyclopedia entry by using a sidebar search box. From any page of encyclopedia user could text request into searchbox and press `Enter`.
If there is one exact the same as requested entry in encyclopedia - user would be redirected to it. If there is more than one entry which title includes as a substring the user's query then user would see the search page with the list of results.
User is able to create it's own entry by clicking **_Create new Page_** link. After clickin, user would be redirected to new page editor. User should provide the title of the new entry and the description. The description should be provided with Markdown syntax.
After submiting information to the encyclopedia user could see 2 different pages. If user submit successfully a new entry, then the entry page would be openned. If user submit information about already existing entry (the title are exactly the same), the error page would be oppened with proposal to edit existig page instead of adding duplicate entry.
There is one more option in encyclopedia. User could open random page by clicking **_Random Page_** in sidebar from any pages of encyclopedia.



