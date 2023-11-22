import spacy
import json
from .utils import *

nlp = spacy.load("en_core_web_lg")


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


def linkSpacyLabels():
    labelsLinked = linkMatched()
    labelsLinked.update(linkUnmatched())
    return labelsLinked


def linkMatched():
    labels_dict = {}
    matched_labels = readFile("../documents/spacy_matched.txt").splitlines()
    for matched in matched_labels:
        labels_dict[matched] = matched
    return labels_dict


def linkUnmatched():
    # match unmatched manuelt

    labels_dict = {}
    unmatched_labels = readFile("../documents/spacy_unmatched.txt").splitlines()
    ontology_classes = readFile("../documents/ontology_classes.txt").splitlines()

    def matchLabel(label):
        label_index = unmatched_labels.index(label)
        labels_dict[unmatched_labels[label_index]] = ontology_classes[class_index]
        unmatched_labels.remove(label)
        
    #Match label med link i steden for index
        label_mapping = {
            "fac": "https://dbpedia.org/ontology/Building",
            "gpe": "https://dbpedia.org/ontology/Country",
            "loc": "https://dbpedia.org/ontology/Location",
            "norp": "https://dbpedia.org/ontology/Group",
            "org": "https://dbpedia.org/ontology/Organisation",
            "product": "https://www.w3.org/2002/07/owl#/thing",
            "work_of_art": "https://dbpedia.org/ontology/Artwork"
    
        }
        return label_mapping.get(label, None)
       
    '''
    # matchLabel("date", ) #TimePeriod
    matchLabel("fac") #Building
    matchLabel("gpe") #Country
    matchLabel("loc") #Place
    # matchLabel('money', 120)
    matchLabel("norp") #Group
    # matchLabel('ordinal', )
    matchLabel("org") #Organisation
    # matchLabel('percent', )
    matchLabel('product') #Thing i owl
    # matchLabel('quantity', )
    # matchLabel('time', )
    matchLabel("work_of_art", label_to_link["work_of_art"]) #Artwork
    '''
    return labels_dict



'''
def generateTriplesFromJSON(labelsDict, JSONobject):

    jsonFilePath = "../files/test.JSON"

    with open(jsonFilePath, "r") as jsonFile:
        data = json.load(jsonFile)
    

    triples = []
    for obj in JSONobject:
        language = obj["language"]

        for sentence in obj['sentences']:
            sent = nlp(sentence['sentence'])
            ems = sentence['entityMentions']

            #translate from detected language to English
            if language != "en":
                translated_sentence = translateWordToEn(sentence['sentence'], language)
                sent = nlp(translated_sentence)

            for ent in sent.ents:
                dbpedia_uri = linkUnmatched()
                for em in ems:
            
                    # her tjekker du ontology.ttl om ent.label_ er owl:dataypeproperty eller owl:class

                    # if owl:class
                    # dbpedia_path = "http://dbpedia.org/ontology/"
                    # elif owl:datatypeproperty'
                    # dbpedia_path = "http://dbpedia.org/datatype/"
                    # triple = (em['iri'], "rdfs:type/is_a", dbpedia_path + labelsDict.get(ent.label_.lower(), ent.label_))

                    #hvis der ik er noget fra vores ontology, så skal der ik laves en triple
                    #triple = (em['iri'], "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", labelsDict.get(ent.label_.lower(), ent.label_))

                    if dbpedia_uri:
                        triple = (ent.text, "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", dbpedia_uri)
                        triples.append(triple)
                      
    return triples
'''

def generateTriplesFromJSONTEST(labelsDict, JSONobject):
    jsonFilePath = "../files/test.JSON"
    triples = []

    with open(jsonFilePath, "r") as jsonFile:
        data = json.load(jsonFile)

    for obj in JSONobject:
        language = obj["language"]

        for sentence in obj['sentences']:
            sent = nlp(sentence['sentence'])
            ems = sentence['entityMentions']

            # Translate from detected language to English
            if language != "en":
                translated_sentence = translateWordToEn(sentence['sentence'], language)
                sent = nlp(translated_sentence)

            for ent in sent.ents:
                # Use the matchLabel function to get the DBpedia link for the label
                dbpedia_uri = linkUnmatched()
                if dbpedia_uri:
                    triple = (ent.text, "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", dbpedia_uri)
                    triples.append(triple)

    return triples


