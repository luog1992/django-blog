from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from models import Category
from django import forms
# Apply summernote to specific fields.

categories = ((category.name, category.name) for category in Category.objects.all())

class BlogEditor(forms.Form):
    # instead of forms.Textarea
    title = forms.CharField(max_length=100, required=True)
    category = forms.ChoiceField(choices=categories, required=True)
    tags = forms.CharField(max_length=100)
    content = forms.CharField(widget=SummernoteInplaceWidget(), required=True)
