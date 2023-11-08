from .utils import *
import spacy
from rdflib import Graph


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
