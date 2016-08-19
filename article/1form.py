from django import forms
from django_bootstrap_markdown.widgets import MarkdownInput

class PostForm(forms.Form):
    title = forms.CharField()
    markdown = forms.CharField(widget=MarkdownInput)