from functions.ontology import generateOntologyClasses
from functions.spacy import *


def generateTXTfiles():
    generateOntologyClasses()
    generateSpacyLabels()
    generateSpacyMatches()
    generateSpacyUnmatchedExplanations()


# temp
fakeJSON = [{"meget": "meget"}, {"fake": "fake"}]

generateTXTfiles()

labelsDict = linkSpacyLabels()

triples = createMagicUnfinished(labelsDict, fakeJSON)

#print(triples)
translateWord("ligge")

