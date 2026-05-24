from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from prompts.models import Category, Author, Prompt, Comment, Rating


class SearchPromptForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search"}),
        label="",
    )


class SearchAuthorForm(forms.Form):
    display_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
        label="",
    )


class SearchCategoryForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
        label="",
    )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)
        labels = {
            "name": "",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter the name"}),
        }

    def clean_name(self):
        name = self.cleaned_data["name"]
        if Category.objects.filter(name__iexact=name).exists():
            raise ValidationError("This category already exists")
        return name


class AuthorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Author
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "display_name",
        )


class PromptCreateForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Prompt
        fields = ("title", "description", "content", "categories")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        labels = {
            "content": "",
        }
        widgets = {
            "content": forms.Textarea(attrs={"placeholder": "Place your comment here"}),
        }

    def clean_content(self):
        content = self.cleaned_data["content"]
        if not content:
            raise ValidationError("The field couldn't be empty")
        return content


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ("value",)
