import spacy
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

    def matchLabel(label, class_index):
        label_index = unmatched_labels.index(label)
        labels_dict[unmatched_labels[label_index]] = ontology_classes[class_index]
        unmatched_labels.remove(label)

    matchLabel("date", 724)
    matchLabel("fac", 108)
    matchLabel("gpe", 183)
    matchLabel("loc", 518)
    # matchLabel('money', 120)
    matchLabel("norp", 309)
    # matchLabel('ordinal', )
    matchLabel("org", 496)
    # matchLabel('percent', )
    # matchLabel('product', )
    # matchLabel('quantity', )
    # matchLabel('time', )
    matchLabel("work_of_art", 49)
    # print(unmatched_labels)

    return labels_dict


def createMagicUnfinished(labelsDict, JSONfile):
    # Halløj Vi. Denne klasse skal bruge labelsDict (din dictionary) i stedet for de predefinerede ontology_classes herunder. Den skal også tage JSON input i stedet for predefineret tekst.
    ontology_classes = {
        "PERSON",
        "FAC",
        "ORG",
        "DATE",
        "NORP",
    }
    # TODO: Take correct data format (JSON) instead of string

    text = (
        "When Sebastian Thrun started working on self-driving cars at "
        "Google in 2007, few people outside of the company took him "
        "seriously. “I can tell you very senior CEOs of major American "
        "car companies would shake my hand and turn away because I wasn’t "
        "worth talking to,” said Thrun, in an interview with Recode earlier "
        "this week. This happened at the Madison Square Garden in New York City"
    )
    doc = nlp(text)

    triples = [
        (ent.text, "is_a", ent.label_)
        for ent in doc.ents
        if ent.label_ in ontology_classes
    ]

    # for triple in triples:
    # print(triple)

    # TODO: export triples in correct data type

    return triples
