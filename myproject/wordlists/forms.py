# -*- coding: utf-8 -*-
from django import forms

from myproject.wordlists.models import WordList

class WordListForm(forms.ModelForm):
    class Meta:
        model = WordList
        fields = ['title', 'language','description', 'color']

    #list_id = forms.CharField(widget=forms.HiddenInput())
    #title = forms.CharField(max_length=50)
    #language = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea)

