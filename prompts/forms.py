from django import forms

from prompts.models import Prompt


class SearchForm(forms.Form):
    title = forms.CharField(max_length=100, required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search"}), label="")
