from django.urls import path
from prompts.views import index, PromptListView


urlpatterns = [
    path("", index, name="index"),
    path("prompts/", PromptListView.as_view(), name="prompt-list"),
]

app_name = "prompts"