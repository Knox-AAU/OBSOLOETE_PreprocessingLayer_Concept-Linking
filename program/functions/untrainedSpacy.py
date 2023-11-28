import spacy
import json
from .utils import *


nlp = spacy.load("en_core_web_lg")
nlp_da = spacy.load("da_core_news_lg")



def generateSpacyLabels():
    # Collect spaCy labels in array and sets it to lower case. Then saves to file.
    spacy_labelsLC = []
    spacy_labels = nlp.get_pipe("ner").labels
    for label in spacy_labels:
        spacy_labelsLC.append(label.lower())
    writeFile("../documents/spacy_labels.txt", "\n".join(spacy_labelsLC))


def generateSpacyMatches():
    # Compare ontology and spacy labels
    matched_labels = []
    unmatched_labels = []

    # print(readFile("../documents/spacy_labels.txt"))
    spacy_labels = readFile("../documents/spacy_labels.txt").splitlines()
    ontology_classes = readFile("../documents/ontology_classes.txt").splitlines()

    for label in spacy_labels:
        for o_class in ontology_classes:
            if label == o_class:
                matched_labels.append(label)
        if label != matched_labels[-1]:
            unmatched_labels.append(label)

    writeFile("../documents/spacy_matched.txt", "\n".join(matched_labels))
    writeFile("../documents/spacy_unmatched.txt", "\n".join(unmatched_labels))


def generateSpacyUnmatchedExplanations():
    clearFile("../documents/spacy_explanations.txt")

    unmatched_labels = readFile("../documents/spacy_unmatched.txt").splitlines()
    for unmatched in unmatched_labels:
        appendFile(
            "../documents/spacy_explanations.txt",
            "".join(unmatched + ": " + spacy.explain(unmatched.upper())) + "\n",
        )




def linkMatched():
    labels_dict = {}
    matched_labels = readFile("../documents/spacy_matched.txt").splitlines()
    for matched in matched_labels:
        labels_dict[matched] = matched
    return labels_dict




def generateTriplesFromJSON(JSONobject):
    triples = []
    
    # matches the spaCy labels to the ontology classes 
    labels_dict = {
        "fac": "https://dbpedia.org/ontology/Building",
        "gpe": "https://dbpedia.org/ontology/Country",
        "loc": "https://dbpedia.org/ontology/Location",
        "norp": "https://dbpedia.org/ontology/Group",
        "org": "https://dbpedia.org/ontology/Organisation",
        "product": "https://www.w3.org/2002/07/owl#/thing",
        "work_of_art": "https://dbpedia.org/ontology/Artwork",
        "person": "https://dbpedia.org/ontology/Person",
        "per": "https://dbpedia.org/ontology/Person", 
        "misc": "https://www.w3.org/2002/07/owl#/thing"
        
    }

    for obj in JSONobject:

        for sentence in obj['sentences']:
            ems = sentence['entityMentions']
            sentence = sentence['sentence']
            
            for em in ems:
                em_iri = em["iri"]
                em_label = em["label"].lower()
                em_type = em["type"].lower()
                
                if em_type == "entity":
                    #get the value from the dictionary 
                    dbpedia_uri = labels_dict.get(em_label, em_label)  

                    triple = (em_iri, "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", dbpedia_uri)
                    triples.append(triple)
    return triples
                        