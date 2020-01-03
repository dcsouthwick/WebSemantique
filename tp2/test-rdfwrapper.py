from SPARQLWrapper import JSON, SPARQLWrapper2
queryString = "SELECT * WHERE { ?s rdf:type ?o. } limit 10"
# get sparql endpoint from graphDB/setup/repositories link icon
sparql = SPARQLWrapper2("http://192.168.1.232:7200/repositories/swoogle")

sparql.setQuery(queryString)
ret = sparql.query()
print(ret.variables)  
# this is an array consisting of "subj" and "prop"
for binding in ret.bindings :
    # each binding is a dictionary. Let us just print the results
    print("{}: {} (of type {})".format("s",binding[u"s"].value,binding[u"s"].type))
    print("{}: {} (of type {})".format("o",binding[u"o"].value,binding[u"o"].type))
