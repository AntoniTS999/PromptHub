from gc import get_objects
from multiprocessing import context

from django.db.models import Avg
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from prompts.models import Prompt, Author, Category
from django.views import generic
from django.db.models.functions import Round

def index(request: HttpRequest) -> HttpResponse:
    num_prompts = Prompt.objects.all().count()
    num_authors = Author.objects.all().count()
    num_categories = Category.objects.all().count()
    context = {
        "num_prompts": num_prompts,
        "num_authors": num_authors,
        "num_categories": num_categories,
    }
    return render(request, "prompts/index.html", context=context)

class PromptListView(generic.ListView):
    model = Prompt

    def get_queryset(self):
        return (
            Prompt.objects
            .select_related("author")
            .prefetch_related("categories")
            .annotate(avg_rating=Round(Avg("ratings__value"), 2))
        )

