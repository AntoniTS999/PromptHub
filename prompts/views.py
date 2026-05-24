from django.db.models import Avg, Q
from django.http import (HttpRequest,
                         HttpResponse,
                         HttpResponseRedirect)
from django.shortcuts import render, get_object_or_404

from django.urls import reverse_lazy, reverse

from prompts.forms import (
    SearchPromptForm,
    SearchAuthorForm,
    SearchCategoryForm,
    CategoryForm,
    AuthorCreationForm,
    PromptCreateForm,
    CommentForm,
    RatingForm,
)
from prompts.models import Prompt, Author, Category, Comment, Rating
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
        queryset = (
            Prompt.objects.select_related("author")
            .prefetch_related("categories")
            .annotate(avg_rating=Round(Avg("ratings__value"), 1))
        )
        form = SearchPromptForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(title__icontains=form.cleaned_data["title"])
        return queryset


class PromptDetailView(generic.DetailView):
    model = Prompt
    form_class = CommentForm

    def get_context_data(self, *, object_list=None, **kwargs):
        prompt = self.get_object()
        context = super(PromptDetailView, self).get_context_data(**kwargs)
        context["counted"] = prompt.comments.count()
        context["form"] = CommentForm()
        return context

    def get_queryset(self):
        queryset = (
            Prompt.objects.select_related("author")
            .prefetch_related("categories")
            .annotate(avg_rating=Round(Avg("ratings__value"), 1))
        )
        return queryset

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = self.request.user
            comment.prompt = self.object
            comment.save()
            return HttpResponseRedirect(
                reverse("prompts:prompt-detail", kwargs={"pk": self.object.pk})
            )
        context = {
            "form": form,
            "prompt": self.object,
        }
        return render(request, "prompts/prompt_detail.html", context=context)


class PromptCreateView(LoginRequiredMixin, generic.CreateView):
    model = Prompt
    form_class = PromptCreateForm
    template_name = "prompts/prompt_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PromptUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Prompt
    form_class = PromptCreateForm


class PromptDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Prompt
    success_url = reverse_lazy("prompts:prompt-list")
    template_name = "prompts/prompt_delete.html"


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        display_name = self.request.GET.get("display_name", "")
        context["search_form"] = SearchAuthorForm(
            initial={"display_name": display_name}
        )
        return context

    def get_queryset(self):
        queryset = Author.objects.all()
        form = SearchAuthorForm(self.request.GET)
        if form.is_valid():
            data = form.cleaned_data["display_name"]
            if data:
                return queryset.filter(
                    Q(display_name__icontains=data)
                    | Q(username__icontains=data)
                )
        return queryset


class AuthorDetailView(generic.DetailView):
    model = Author


class AuthorCreateView(generic.CreateView):
    model = Author
    form_class = AuthorCreationForm
    success_url = reverse_lazy("login")
    template_name = "prompts/author_form.html"


class AuthorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Author
    form_class = AuthorCreationForm

    def get_success_url(self):
        return reverse_lazy("prompts:author-detail",
                            kwargs={"pk": self.object.pk})


class AuthorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Author
    success_url = reverse_lazy("prompts:author-list")
    template_name = "prompts/author_delete.html"


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


class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "prompts/category_form.html"

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse("prompts:category-list")


class CategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Category
    fields = ("name",)

    def get_success_url(self):
        return reverse_lazy("prompts:category-detail",
                            kwargs={"pk": self.object.pk})


class CategoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Category
    success_url = reverse_lazy("prompts:category-list")
    template_name = "prompts/category_delete.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next"] = self.request.META.get("HTTP_REFERER")
        return context


class CommentUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "prompts/comment_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "prompts:prompt-detail", kwargs={"pk": self.object.prompt.id}
        )


class CommentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Comment
    template_name = "prompts/comment_delete.html"

    def get_success_url(self):
        return reverse_lazy(
            "prompts:prompt-detail", kwargs={"pk": self.object.prompt.pk}
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next"] = self.request.META.get("HTTP_REFERER")
        return context


class RatingCreateView(LoginRequiredMixin, generic.CreateView):
    model = Rating
    form_class = RatingForm

    def get_success_url(self):
        return reverse_lazy("prompts:prompt-detail",
                            kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next"] = self.request.META.get("HTTP_REFERER")
        context["already_rated"] = Rating.objects.filter(
            user=self.request.user, prompt_id=self.kwargs["pk"]
        ).exists()
        context["form"] = RatingForm()
        return context

    def post(self, request, *args, **kwargs):
        prompt = get_object_or_404(Prompt, pk=self.kwargs["pk"])
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.prompt = prompt
            rating.user = request.user
            rating.save()
            return HttpResponseRedirect(
                reverse_lazy("prompts:prompt-detail", kwargs={"pk": prompt.id})
            )
        context = {
            "form": form,
            "prompt": prompt,
        }
        return render(request, "prompts/rating_form.html", context=context)
