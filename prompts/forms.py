from django import forms

from prompts.models import Prompt


class SearchPromptForm(forms.Form):
    title = forms.CharField(max_length=100, required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search"}), label="")

class SearchAuthorForm(forms.Form):
    display_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={"placeholder": "Search by username"}), label="")