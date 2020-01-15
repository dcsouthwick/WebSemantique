from django import forms

class SearchForm(forms.Form):
    search = forms.CharField(label='Search', initial="Project", help_text="keyword search", max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    query = forms.CharField(label="RDF Query", widget=forms.Textarea(), max_length=255, help_text="includes prefixes like rdf, owl, tp2c", required=False)
    # SELECT * WHERE { ?s ?p ?o. } limit 10