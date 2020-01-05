# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from SPARQLWrapper import JSON, SPARQLWrapper2
from requests import Timeout
import django_tables2 as tables

sparql = SPARQLWrapper2("http://192.168.1.232:7200/repositories/swoogle")
sparql.setTimeout(2)

class HomePageView(TemplateView):
    template_name = 'home.html'

class SearchResultsView(TemplateView):
    template_name = 'search_results.html'
    
    def query(self):
        return self.request.GET.get('q', '')
    
    def query_result(self):
        query = self.request.GET.get('q', '')
        sparql.setQuery(query)
    
        try:
            response = sparql.query()
        except TimeoutError:
            return -1
        except Exception as e:
            print(e)
            return -1
        attrs = {}
        for k in response.variables:
            attrs[str(k)] = tables.Column()
        responseTable = type('responseTable', (tables.Table,), attrs)
        DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap4.html"
        return responseTable(response.bindings)
        