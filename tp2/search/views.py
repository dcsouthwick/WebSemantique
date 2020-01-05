# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from SPARQLWrapper import JSON, SPARQLWrapper2
from requests import Timeout
import django_tables2 as tables
from nltk import PorterStemmer

sparql = SPARQLWrapper2("http://192.168.1.232:7200/repositories/swoogle")
sparql.setTimeout(2)

class HomePageView(TemplateView):
    template_name = 'home.html'

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
        prefix = "PREFIX : <http://cui.unige.ch/isi/swt/tp2c#>  "
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
        