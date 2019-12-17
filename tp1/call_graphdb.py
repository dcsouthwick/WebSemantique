from urllib.parse import quote
from urllib.request import urlopen

repositoryHost = "http://localhost:7200/repositories/"
repositoryName = "RepProva"
repositoryUrl = repositoryHost + repositoryName + "?query="

queryTest = "SELECT DISTINCT ?class WHERE { ?s a ?class }"
# queryTest = "SELECT (?s AS ?Organization) (COUNT(?o) AS ?Count) WHERE{ ?s ?p ?o  . } GROUP BY ?s"

print("query to be executed: " + queryTest)
queryTest = quote(queryTest) # encode the query to avoid http errors. Remove white spaces and special characters like " ", &, {, etc
url = repositoryUrl + queryTest  # http://localhost:7200/repositories/rep-prova?query=SELECT%20DISTINCT%20%3Fclass%20WHERE%20%7B%3Fs%20a%20%3Fclass%7D
print("calling: " + url)
htmlAsByte = urlopen(url).read()

print("result : " + str(htmlAsByte))
