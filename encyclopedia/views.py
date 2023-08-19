from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template import Context, Template
from . import util
from encyclopedia.forms import CreateForm, EditForm
import json
import re
import random



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def goto(request, title):
    content = util.converted_entry(title)
    if (content is None):
        return render(request, "encyclopedia/error.html")
    return render(request, "encyclopedia/goto.html", {
        "content": content,
        "title": title,
        "text": content,
    })

def search(request):
    bite = request.body
    encoding = 'ISO-8859-1'
    stringedQuery = bite.decode(encoding)
    query = stringedQuery.split('=')
    entries = util.search_entries(query[2])
    
    content = util.get_entry(query[2])
    
    if entries == []:
        return render(request, "encyclopedia/error.html")

    if content:
        return render(request, "encyclopedia/goto.html", {
            "content": content, 
        })                                  
    else:
        return render(request, "encyclopedia/search.html", {
            "title": query[2],
            "entries": entries,
        })

def create(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            
            if (util.get_entry(title)):
                messages.error(request, f"An entry with the title {title} already exists. Please choose another title.")
            else:
                util.save_entry(title, content)
                return goto(request, title)
    return render(request, "encyclopedia/create.html", {
        "all": CreateForm()
    })


def edit(request):
    if request.method == 'POST':
        data = request.POST
        content = util.get_entry(data['title'])
        form = EditForm(initial={'title': data['title'], 'content': content})
        return render(request, 'encyclopedia/edit.html', {
            "title": data['title'],
            "all": form,
        })
    
def editreal(request):
    if request.method == 'POST':
        data = request.POST
        util.save_entry(data['title'], data['content'])
        return goto(request, data['title'])

def randomPage(request):
    listEntries =  util.list_entries()
    randomMd = random.choice(listEntries)

    return goto(request, randomMd)

def markdownify(title):
    # opening file \[(.*)\]\(/wiki/(.*)\)
    with open(f"entries/{title}.md") as file:
        # reading into the file
        reading_file = file.read()
        # converting markdown heading to html heading
        for i in range(6, 0, -1):
            reading_file = re.sub(fr"{'#' * i}(.*)", fr"<h{i}>\1</h{i}>", reading_file)
            
        # converting markdown boldface text into html boldface text
        reading_file = re.sub(r'\*\*(.*?)\*\*', r"<b>\1</b>", reading_file)

        # converting markdown italic into html italic text
        reading_file = re.sub(r'_(.*?)_', r"<i>\1</i>", reading_file)
        reading_file = re.sub(r'\*(.*?)\*', r"<i>\1</i>", reading_file)  

        # converting markdown unordered lists into html unordered lis  
        reading_file = re.sub(r'[-+*]\s+(.*)', r'<li>\1</li>', reading_file, flags=re.MULTILINE)
        
        reading_file = re.sub(r'(<li>.*</li>)', fr'<ul>\1', reading_file, 1) 
        reading_file = re.sub(r'</li>(?![\s\S]*</li>)', '</li></ul>', reading_file)  

        # converting markdown links into html links
        reading_file = re.sub(r'\[(.*?)\]\((.*?)\)', r'''<a href="\2">\1</a>''', reading_file)

        # add a paragraph tag
        # reading_file = re.sub(r"(The most.*)", r"<p>\1</p>", reading_file, flags=re.DOTALL)

        return reading_file 