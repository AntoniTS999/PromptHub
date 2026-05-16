from django.urls import path
from prompts.views import index, PromptListView, AuthorListView, CategoryListView


urlpatterns = [
    path("", index, name="index"),
    path("prompts/", PromptListView.as_view(), name="prompt-list"),

    path("authors/", AuthorListView.as_view(), name="author-list"),

    path("categories/", CategoryListView.as_view(), name="category-list"),
]

app_name = "prompts"