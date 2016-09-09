# encoding: utf-8
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from models import Category
from django import forms

categories = ((category.name, category.name)
              for category in Category.objects.all())


class BlogEditor(forms.Form):
    # instead of forms.Textarea
    title = forms.CharField(max_length=100, required=True)
    category = forms.ChoiceField(choices=categories, required=True)
    tags = forms.CharField(max_length=100, required=False)
    content = forms.CharField(widget=SummernoteWidget(), required=True)

    def clean_content(self):
        print '....clean_content is called'
        content = self.cleaned_data['content']
        if len(content) <= 4:
        	# because of the summernote editor, the min length of content would be 4 when it's blank
            raise forms.ValidationError('蠢货，多写几个字啊')
        return content


class CategoryForm(forms.Form):
    name = forms.CharField(label='Category Name', max_length=20)
    color = forms.CharField(label='Category Color', max_length=20)
    public = forms.BooleanField(label='Public Category')


class TestForm(forms.Form):
    subject = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(max_length=1000, required=True)
