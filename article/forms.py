from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django import forms
# Apply summernote to specific fields.


class BlogEditor(forms.Form):
    # instead of forms.Textarea
    title = forms.CharField(max_length=100, required=True)
    category = forms.ChoiceField()
    # category = forms.CharField(max_length=20)
    tags = forms.CharField(max_length=100)
    content = forms.CharField(widget=SummernoteInplaceWidget())
