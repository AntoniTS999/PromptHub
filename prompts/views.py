from gc import get_objects
from multiprocessing import context

from django.db.models import Avg
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from prompts.forms import SearchForm
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PromptListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = SearchForm(initial={"title": title})
        return context

    def get_queryset(self):
        queryset = (Prompt.objects.select_related("author")
                    .prefetch_related("categories")
                    .annotate(avg_rating=Round(Avg("ratings__value"),
                                               2)))
        form = SearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(title__icontains=form.cleaned_data["title"])
        return queryset


class AuthorListView(generic.ListView):
    model = Author