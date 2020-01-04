Web Semantique Autumn 2019
==================
##### Masters course for University of Geneva, Switzerland

This repository consists of the two semester group projects
### TP1

#### TP2
A project to extract knowledge from various RDF resources with unrelated ontologies.
Webserver based on django searching an RDFstore (graphDB) using a constructed generalized ontology.

**Setup:**
Locate your RDFstore (graphDB connection string) and put it into
tp2/search/views.py: 
```sh
sparql = SPARQLWrapper2("http://192.168.1.232:7200/repositories/swoogle")
```

Launching the web interface:
```sh
cd tp2/
pipenv
pipenv run python manage.py runserver
```
navigate to localhost:8000 and search away. 