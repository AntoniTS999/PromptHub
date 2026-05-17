from django.urls import path
from prompts.views import (index, PromptListView,
                           PromptDetailView,
                           AuthorListView,
                           AuthorDetailView,
                           CategoryListView,
                           CategoryDetailView,
                           CategoryCreateView
                           )


urlpatterns = [
    path("", index, name="index"),

    path("prompts/", PromptListView.as_view(), name="prompt-list"),
    path("prompts/<int:pk>/", PromptDetailView.as_view(), name="prompt-detail"),

    path("authors/", AuthorListView.as_view(), name="author-list"),
    path("authors/<int:pk>", AuthorDetailView.as_view(), name="author-detail"),

    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/<int:pk>", CategoryDetailView.as_view(), name="category-detail"),
    path("categories/create/", CategoryCreateView.as_view(), name="category-create"),
]

app_name = "prompts"