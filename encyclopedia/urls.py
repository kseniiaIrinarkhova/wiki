from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entries, name="entry" ),
    path("search", views.search, name="search"),
    path("new_entry", views.addEntry, name="new_entry"),
    path("wiki/edit/<str:entry>", views.changeEntry, name="editor" ),
    path("random", views.randomEntry, name="random")
]
