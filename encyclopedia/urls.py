from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry_detail, name="entry_detail"),
    path("wiki/", views.random_entry, name="random_entry"),
    path("search/", views.search, name="search"),
    path("new_page/", views.new_page, name="new_page"),
    path("edit_entry/", views.edit_entry, name="edit_entry"),
]
