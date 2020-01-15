from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class SearchForm(forms.Form):
    search = forms.CharField(label='Search', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    query = forms.CharField(widget=forms.Textarea(), cols="60", rows="4", placeholder="SELECT * WHERE { ?s ?p ?o. }")