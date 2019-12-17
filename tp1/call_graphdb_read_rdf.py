from urllib.parse import quote
from urllib.request import urlopen
from xml.dom import minidom

repositoryHost = "http://localhost:7200/repositories/"
repositoryName = "rep-prova"
repositoryUrl = repositoryHost + repositoryName + "?query="

queryTest = "SELECT DISTINCT ?class WHERE { ?s a ?class }"
# queryTest = "SELECT (?s AS ?Organization) (COUNT(?o) AS ?Count) WHERE{ ?s ?p ?o  . } GROUP BY ?s"

print("query to be executed: " + queryTest)
queryTest = quote(queryTest) # encode the query to avoid http errors. Remove white spaces and special characters like " ", &, {, etc
url = repositoryUrl + queryTest  # http://localhost:7200/repositories/rep-prova?query=SELECT%20DISTINCT%20%3Fclass%20WHERE%20%7B%3Fs%20a%20%3Fclass%7D
print("calling: " + url)
xmlAsByte = urlopen(url).read()
xml = str(xmlAsByte)
xml = xml.replace('\\r', "\r", 99999) # for some reason the special character \r is coming as string. replace it everywhere
xml = xml.replace('\\n', "\n", 99999) # same for \n (new line character)

out_file = open("xmlResult.xml", "w+")
out_file.write(xml)

print("result : ")
