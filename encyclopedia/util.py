import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from . import views

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def search_entries(query):
    """
    Return a list of entries based on the search query
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if re.search(query, filename, re.IGNORECASE) and filename.endswith(".md")))

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

def save_edited(title, newtitle, content):
    filename = f"entries/{title}.md"
    newfilename = f"entries/{newtitile}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(newfilename, ContentFile(content))

def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    _, filenames = default_storage.listdir("entries")
    file_case = re.search(title, str(filenames), re.IGNORECASE)
    if file_case is None:
        return None
    try:
        f = default_storage.open(f"entries/{file_case.group()}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def converted_entry(title):
    _, filenames = default_storage.listdir("entries")
    file_case = re.search(title, str(filenames), re.IGNORECASE)
    print(file_case)
    if file_case is None:
        return None
    try:
        f = default_storage.open(f"entries/{file_case.group()}.md")
        fi = f.read().decode("utf-8")
        converted = views.markdownify(title)
        return converted
    except FileNotFoundError:
        return None