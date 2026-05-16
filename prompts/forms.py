from django import forms


class SearchPromptForm(forms.Form):
    title = forms.CharField(max_length=100, required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search"}), label="")

class SearchAuthorForm(forms.Form):
    display_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={"placeholder": "Search by name"}), label="")

class SearchCategoryForm(forms.Form):
    name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={"placeholder": "Search by name"}), label="")