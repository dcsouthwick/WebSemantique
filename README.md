# WebSemantique
Autumn 2019 WebSemantique for UNIGE

This repository consists of the two semester group projects


tp2:
Webserver based on django searching various RDF files.


setup:
Locate your RDFstore (graphDB connection string) and put it into
tp2/search/views.py: 
`sparql = SPARQLWrapper2("http://192.168.1.232:7200/repositories/swoogle")`

Launching the web interface:
```
cd tp2/
pipenv
pipenv run python manage.py runserver
```
navigate to localhost:8000 and search away. 