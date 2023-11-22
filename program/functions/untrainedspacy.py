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

    def matchLabel(label, path):
        #tilføj owl link
     
            # tilføj ontology/
            label_index = unmatched_labels.index(label)
            labels_dict[unmatched_labels[label_index]] = ontology_classes[class_index]
            unmatched_labels.remove(label)

    #Match label med link i steden for index

    # matchLabel("date", 724) #TimePeriod
    matchLabel("fac", 108) #Building
    matchLabel("gpe", 183) #Country
    matchLabel("loc", 518) #Place
    # matchLabel('money', 120)
    matchLabel("norp", 309) #Group
    # matchLabel('ordinal', )
    matchLabel("org", 496) #Organisation
    # matchLabel('percent', )
    matchLabel('product', NULL, "https://www.w3.org/2002/07/owl#/thing") #Thing i owl
    # matchLabel('quantity', )
    # matchLabel('time', )
    matchLabel("work_of_art", 49) #Artwork


    return labels_dict


def createMagicUnfinished(labelsDict, JSONobject):

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
                for em in ems:
                    print('ent.label_: ', ent.label_)

                    # her tjekker du ontology.ttl om ent.label_ er owl:dataypeproperty eller owl:class

                    # if owl:class
                    # dbpedia_path = "http://dbpedia.org/ontology/"
                    # elif owl:datatypeproperty'
                    # dbpedia_path = "http://dbpedia.org/datatype/"
                    # triple = (em['iri'], "rdfs:type/is_a", dbpedia_path + labelsDict.get(ent.label_.lower(), ent.label_))

                    #hvis der ik er noget fra vores ontology, så skal der ik laves en triple

                    triple = (em['iri'], "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", labelsDict.get(ent.label_.lower(), ent.label_))

                    triples.append(triple)
                      
    return triples

