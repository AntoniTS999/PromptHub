from django.urls import path
from prompts.views import index

urlpatterns = [
    path("", index, name="index"),
]

app_name = "prompts"