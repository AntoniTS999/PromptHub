from django.urls import path
from prompts.views import (index, PromptListView,
                           PromptDetailView,
                           AuthorListView,
                           AuthorDetailView,
                           AuthorCreateView,
                           CategoryListView,
                           CategoryDetailView,
                           CategoryCreateView,
                           CategoryUpdateView,
                           CategoryDeleteView,
                           )


urlpatterns = [
    path("", index, name="index"),

    path("prompts/", PromptListView.as_view(), name="prompt-list"),
    path("prompts/<int:pk>/", PromptDetailView.as_view(), name="prompt-detail"),

    path("authors/", AuthorListView.as_view(), name="author-list"),
    path("authors/<int:pk>", AuthorDetailView.as_view(), name="author-detail"),
    path("authors/create/", AuthorCreateView.as_view(), name="author-create"),

    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/<int:pk>", CategoryDetailView.as_view(), name="category-detail"),
    path("categories/create/", CategoryCreateView.as_view(), name="category-create"),
    path("categories/<int:pk>/update/", CategoryUpdateView.as_view(), name="category-update"),
    path("categories/<int:pk>/delete/", CategoryDeleteView.as_view(), name="category-delete"),
]

app_name = "prompts"