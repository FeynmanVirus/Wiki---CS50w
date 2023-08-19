from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.goto, name="title"),
    path("search/", views.search, name="search"),
    path("create/", views.create, name="create"),
    path("edit/", views.edit, name="edit"),
    path("editreal/", views.editreal, name="editreal"),
    path("random/", views.randomPage, name="randomPage")
]
