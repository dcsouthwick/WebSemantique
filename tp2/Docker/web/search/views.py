# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, FormView
from SPARQLWrapper import JSON, SPARQLWrapper2
from requests import Timeout
import django_tables2 as tables
from nltk import PorterStemmer
from search.forms import SearchForm

sparql = SPARQLWrapper2("http://graphDB:7200/repositories/swoogle")
sparql.setTimeout(2)

class HomePageView(FormView):
    template_name = 'home.html'
    form_class = SearchForm

class SearchResultsView(TemplateView):
    template_name = 'search_results.html'
    
    def query(self):
        query = self.request.GET.get('q', '')
        search = self.request.GET.get('s', '')
        return query or self.sparqlQuery(search)
    
    def sparqlQuery(self, search):
        query = f"SELECT ?{search} ?name WHERE {{ ?{search} a :{search}. ?{search} :hasName ?name. }}"
        return query
 
    def stem(self, phrase):
        return PorterStemmer().stem(phrase)



    def query_result(self):
        prefix = "PREFIX : <http://cui.unige.ch/isi/swt/tp2#>  "
        query = prefix+self.query()
        sparql.setQuery(query)
    
        try:
            response = sparql.query()
        except TimeoutError:
            raise TimeoutError
        except Exception as e:
            print(e)
            raise e
        attrs = {}
        for k in response.variables:
            attrs[str(k)] = tables.Column()
        responseTable = type('responseTable', (tables.Table,), attrs)
        return responseTable(response.bindings)
        