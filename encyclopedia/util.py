import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

import markdown2

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

'''
global dictionary of errors' texts *n* is template for dynamic data
'''
errors = {
    "404" : f"Sorry, there is no information about <b>*1*</b> in our encyclopedia...",
    "search": f"There is no result for <b>*1*</b>. Try another keywords.",
    "empty": "You must input the search value."
}

def convert_markdown(title):
    """
    Convert entry information from Markdown to Html
    """
    description = get_entry(title)
    if description is None:
        return description
    return markdown2.markdown(description)

def list_entries_with_parameter(search_entry):
    """
    Returns a list of all names of encyclopedia entries 
    according to the search parameter.
    """
    filter = re.compile(r"\w*"+search_entry+r"\w*",  re.IGNORECASE)
    all_entries=list_entries()
    return list(sorted(entry for entry in all_entries if filter.search(entry) is not None ))

