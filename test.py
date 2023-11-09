import spacy
from rdflib import Graph

g = Graph()
g.parse("ontology.ttl", format="ttl")

# TODO: Get all correct classes from ontology. 
# se om ontology og spacy classerne er de samme, hvis nej print listen for dem
query = """
    SELECT DISTINCT ?class
    WHERE {
        ?class a owl:Class .
    }
"""

results = g.query(query)
ontology_classes = [str(result['class']) for result in results]

# Collect ontology classes in array and sets it to lower case. Then saves to file.

ontology_classesLC = []
for ontology_class in ontology_classes:
    ontology_classesLC.append(ontology_class.removeprefix("http://dbpedia.org/ontology/").lower())
with open('ontology_classes.txt', 'w') as f:
    f.write("\n".join(ontology_classesLC))

# Collect spaCy labels in array and sets it to lower case. Then saves to file.
nlp = spacy.load("en_core_web_lg")
print(nlp)
spacy_labelsLC = []
spacy_labels = nlp.get_pipe("ner").labels
for label in spacy_labels:
    spacy_labelsLC.append(label.lower())
with open('spacy_labels.txt', 'w') as f:
    f.write("\n".join(spacy_labelsLC))

# Compare ontology and spacy labels
matched_labels = []
unmatched_labels = []
for label in spacy_labelsLC:
    for o_class in ontology_classesLC:
        if label == o_class:
            matched_labels.append(label)
    if label != matched_labels[-1]:
        unmatched_labels.append(label)


print(matched_labels)
print(unmatched_labels)

with open('spacy_explanations.txt', 'w') as f:
        f.write("")
for unmatched in unmatched_labels:
    print(unmatched + ": " + spacy.explain(unmatched.upper()))
    with open('spacy_explanations.txt', 'a') as f:
        f.write("".join(unmatched + ": " + spacy.explain(unmatched.upper())))
        f.write("\n")

#match unmatched manualt 
labels_dict = {}
for matched in matched_labels:
    labels_dict[matched] = matched



def matchLabel(label, class_index):
    label_index = unmatched_labels.index(label)
    print(label_index)
    labels_dict[unmatched_labels[label_index]] = ontology_classesLC[class_index]
    unmatched_labels.remove(label)


matchLabel('date', 724)
matchLabel('fac', 108)
matchLabel('gpe', 183)
matchLabel('loc', 518)
# matchLabel('money', 120)
matchLabel('norp', 309)
# matchLabel('ordinal', )
matchLabel('org', 496)
# matchLabel('percent', )
# matchLabel('product', )
# matchLabel('quantity', )
# matchLabel('time', )
matchLabel('work_of_art', 49)
print(unmatched_labels)




ontology_classes = {
    'PERSON', 
    'FAC', 
    'ORG',
    'DATE',
    'NORP',
}




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