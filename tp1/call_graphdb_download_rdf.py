from urllib.parse import quote
from urllib.request import urlopen
from xml.dom import minidom
import urllib.request

repositoryHost = "http://localhost:7200/repositories/"
repositoryName = "rep-prova"
repositoryUrl = repositoryHost + repositoryName + "?query="

queryTest = "SELECT DISTINCT ?class WHERE { ?s a ?class }"
# queryTest = "SELECT (?s AS ?Organization) (COUNT(?o) AS ?Count) WHERE{ ?s ?p ?o  . } GROUP BY ?s"

print("query to be executed: " + queryTest)
queryTest = quote(queryTest) # encode the query to avoid http errors. Remove white spaces and special characters like " ", &, {, etc
url = repositoryUrl + queryTest  # http://localhost:7200/repositories/rep-prova?query=SELECT%20DISTINCT%20%3Fclass%20WHERE%20%7B%3Fs%20a%20%3Fclass%7D
print("calling: " + url)

urllib.request.urlretrieve(url, 'xmlResult2.xml')
htmlStart = "<html>"
htmlContent = ""  # build html with the data or xmlResult2.xml
htmlEnd = "</html>"

# xmlResult = minidom.parse('xmlResult2.xml')
# items = xmlResult.getElementsByTagName('item') # tag name that Esi will say
# #print(items[1].attributes['name'].value)
#
# # all item attributes
# print('\nAll attributes:')
# for elem in items:
#     print(elem.attributes['name'].value)
#     # enrich the outer html file we are going to build


html_file = open("rdf_html.html", "w+")
html = htmlStart + htmlContent + htmlEnd
html_file.write(html)

print("END")
