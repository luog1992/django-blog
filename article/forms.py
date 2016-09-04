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
    content = forms.CharField(widget=SummernoteWidget(), required=True)


class TestForm(forms.Form):
	subject = forms.CharField(max_length=50, required=True)
	email = forms.EmailField(required=True)
	message = forms.CharField(max_length=1000, required=True)

