from django.db.models import Avg, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from prompts.forms import SearchPromptForm, SearchAuthorForm, SearchCategoryForm, CategoryForm, AuthorCreationForm
from prompts.models import Prompt, Author, Category
from django.views import generic
from django.db.models.functions import Round
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request: HttpRequest) -> HttpResponse:
    num_prompts = Prompt.objects.all().count()
    num_authors = Author.objects.all().count()
    num_categories = Category.objects.all().count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    context = {
        "num_prompts": num_prompts,
        "num_authors": num_authors,
        "num_categories": num_categories,
        "num_visits": num_visits + 1,
    }
    return render(request, "prompts/index.html", context=context)

class PromptListView(generic.ListView):
    model = Prompt
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PromptListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = SearchPromptForm(initial={"title": title})
        return context

    def get_queryset(self):
        queryset = (Prompt.objects.select_related("author")
                    .prefetch_related("categories")
                    .annotate(avg_rating=Round(Avg("ratings__value"),
                                               1)))
        form = SearchPromptForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(title__icontains=form.cleaned_data["title"])
        return queryset

class PromptDetailView(generic.DetailView):
    model = Prompt

    def get_context_data(self, *, object_list=None, **kwargs):
        prompt = self.get_object()
        context = super(PromptDetailView, self).get_context_data(**kwargs)
        context["counted"] = prompt.comments.count()
        return context

    def get_queryset(self):
        queryset = Prompt.objects.select_related("author").prefetch_related("categories").annotate(avg_rating=Round(Avg("ratings__value"),1))
        return queryset



class AuthorListView(LoginRequiredMixin,generic.ListView):
    model = Author
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        display_name = self.request.GET.get("display_name", "")
        context["search_form"] = SearchAuthorForm(initial={"display_name": display_name})
        return context

    def get_queryset(self):
        queryset = Author.objects.all()
        form = SearchAuthorForm(self.request.GET)
        if form.is_valid():
            data = form.cleaned_data["display_name"]
            if data:
                return queryset.filter(
                    Q(display_name__icontains=data) |
                    Q(username__icontains=data)
                )
        return queryset

class AuthorDetailView(generic.DetailView):
    model = Author

class AuthorCreateView(LoginRequiredMixin,generic.CreateView):
    model = Author
    form_class = AuthorCreationForm
    success_url = reverse_lazy("prompts:author-list")
    template_name = "prompts/author_form.html"

class CategoryListView(generic.ListView):
    model = Category
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = SearchCategoryForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Category.objects.prefetch_related("prompts")
        form = SearchCategoryForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset

class CategoryDetailView(generic.DetailView):
    model = Category

class CategoryCreateView(LoginRequiredMixin,generic.CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy("prompts:category-list")
    template_name = "prompts/category_form.html"

class CategoryUpdateView(LoginRequiredMixin,generic.UpdateView):
    model = Category
    fields = ("name",)

    def get_success_url(self):
        return reverse_lazy("prompts:category-detail", kwargs={"pk": self.object.pk})

class CategoryDeleteView(LoginRequiredMixin,generic.DeleteView):
    model = Category
    success_url = reverse_lazy("prompts:category-list")
    template_name = "prompts/category_delete.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next"] = self.request.META.get("HTTP_REFERER")
        return context
