# encoding: utf-8
import re

from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from models import Category
from django import forms

categories = ((category.name, category.name)
              for category in Category.objects.get_valid_categories())

def color_checker(color):
    color = color.strip('#')
    patt = re.compile(r'\w{6}', re.I)
    findall = patt.findall(color[:6])
    return findall


class BlogEditor(forms.Form):
    title = forms.CharField(max_length=100, required=True)
    category = forms.ChoiceField(choices=categories, required=True)
    tags = forms.CharField(max_length=100, required=False)
    content = forms.CharField(widget=SummernoteWidget(), required=True)

    def clean_content(self):
        print '....clean_content is called'
        content = self.cleaned_data['content']
        if len(content) <= 4:
                # because of the summernote editor, the min length of content
                # would be 4 when it's blank
            raise forms.ValidationError('蠢货，多写几个字啊')
        return content


class CategoryForm(forms.Form):
    name = forms.CharField(label='Category Name', max_length=20)
    color = forms.CharField(label='Category Color', max_length=20)
    public = forms.BooleanField(label='Public Category', required=False)

    def clean_color(self):
        color = self.cleaned_data['color']
        if not color_checker(color):
            raise forms.ValidationError('Invalid Color Format')
        return color



class TagForm(forms.Form):
    name = forms.CharField(label='Tag Name', max_length=20)
    color = forms.CharField(label='Tag Color', max_length=20)

    def clean_color(self):
        color = self.cleaned_data['color']
        if not color_checker(color):
            raise forms.ValidationError('Invalid Color Format')
        return color


class TestForm(forms.Form):
    subject = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(max_length=1000, required=True)
