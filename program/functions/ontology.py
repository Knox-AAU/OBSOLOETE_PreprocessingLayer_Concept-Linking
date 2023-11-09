from .utils import *
from rdflib import Graph, URIRef, Namespace


def generateOntologyClasses():
    g = Graph()
    g.parse("files/ontology.ttl", format="ttl")

    # TODO: Get all correct classes from ontology.
    # se om ontology og spacy classerne er de samme, hvis nej print listen for dem
    query = """
        SELECT DISTINCT ?class
        WHERE {
            ?class a owl:Class .
        }
    """

    results = g.query(query)
    ontology_classes = [str(result["class"]) for result in results]

    # Collect ontology classes in array and sets it to lower case. Then saves to file.
    ontology_classesLC = []
    for ontology_class in ontology_classes:
        ontology_classesLC.append(
            ontology_class.removeprefix("http://dbpedia.org/ontology/").lower()
        )
    writeFile("../documents/ontology_classes.txt", "\n".join(ontology_classesLC))

def queryLabels():
    g = Graph()
    g.parse("files/ontology.ttl", format="ttl")

    qres = g.query( """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>

    SELECT ?class (lang(?label) as ?language) ?label
    WHERE {
        ?class a owl:Class .
        ?class rdfs:label ?label .
    } 
    """ )

    classesDict = {}
    for row in qres:
        r = str(row).split()

        #prov:Revision i ontology bliver til provRevision. Hvad er prov?
        className = "".join(c for c in r[0] if c.isalpha()).removeprefix("rdflibtermURIRefhttpdbpediaorgontology")
        labelLang = "".join(c for c in r[1] if c.isalpha()).removeprefix("rdflibtermLiteral")
        label = "".join(c for c in r[2] if c.isalpha()).removeprefix("rdflibtermLiteral")
        if className not in classesDict:
            classesDict[className] = []
        classesDict[className].append({labelLang: label})
    
    #with open("../documents/ontology_CL.txt", 'w') as f:
     #   for key, value in classesDict.items():
      #      f.write(f'{key}: {value}\n')
    
    return classesDict
