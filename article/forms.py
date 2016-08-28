from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django import forms
# Apply summernote to specific fields.


class BlogEditor(forms.Form):
    # instead of forms.Textarea
    title = forms.CharField()
    tags = forms.CharField()
    content = forms.CharField(widget=SummernoteWidget())

# If you don't like <iframe>, then use inplace widget
# Or if you're using django-crispy-forms, please use this.


class AnotherForm(forms.Form):
    bar = forms.CharField(widget=SummernoteInplaceWidget())
