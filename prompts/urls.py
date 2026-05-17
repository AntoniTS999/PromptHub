from django.urls import path
from prompts.views import (index, PromptListView,
                           PromptDetailView,
                           AuthorListView,
                           AuthorDetailView,
                           CategoryListView,
                           )


urlpatterns = [
    path("", index, name="index"),

    path("prompts/", PromptListView.as_view(), name="prompt-list"),
    path("prompts/<int:pk>/", PromptDetailView.as_view(), name="prompt-detail"),

    path("authors/", AuthorListView.as_view(), name="author-list"),
    path("authors/<int:pk>", AuthorDetailView.as_view(), name="author-detail"),

    path("categories/", CategoryListView.as_view(), name="category-list"),
]

app_name = "prompts"