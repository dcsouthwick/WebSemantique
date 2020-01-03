from django.views.generic import TemplateView
from SPARQLWrapper import JSON, SPARQLWrapper2

class HomePageView(TemplateView):
    template_name = 'home.html'

class SearchResultsView(TemplateView):
    template_name = 'search_results.html'
   
    def query(self):
        return self.request.GET.get('q', '')
    
    def query_result(self):
        q = self.request.GET.get('q', '')
        sparql = SPARQLWrapper2("http://192.168.1.232:7200/repositories/swoogle")
        sparql.setQuery(q)
        ret = sparql.query()

        return ret