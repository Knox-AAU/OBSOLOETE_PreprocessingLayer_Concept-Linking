import spacy
from rdflib import Graph

g = Graph()
g.parse("ontology.ttl", format="ttl")

# TODO: Get all correct classes from ontology. 

query = """
    SELECT DISTINCT ?class
    WHERE {
        ?class a owl:Class .
    }
"""

results = g.query(query)
ontology_classes = [str(result['class']) for result in results]

print(ontology_classes)

ontology_classes = {
    'PERSON', 
    'FAC', 
    'ORG',
    'DATE',
    'NORP',
}

nlp = spacy.load("en_core_web_sm")

# TODO: Take correct data format (JSON) instead of string

text = ("When Sebastian Thrun started working on self-driving cars at "
        "Google in 2007, few people outside of the company took him "
        "seriously. “I can tell you very senior CEOs of major American "
        "car companies would shake my hand and turn away because I wasn’t "
        "worth talking to,” said Thrun, in an interview with Recode earlier "
        "this week. This happened at the Madison Square Garden in New York City")
doc = nlp(text)

triples = [(ent.text, 'is_a', ent.label_) for ent in doc.ents if ent.label_ in ontology_classes]

for triple in triples:
    print(triple)

# TODO: export triples in correct data type