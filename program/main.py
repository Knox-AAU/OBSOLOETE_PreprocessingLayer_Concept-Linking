from functions.ontology import *
from functions.spacy import *


def generateTXTfiles():
    generateOntologyClasses()
    generateSpacyLabels()
    generateSpacyMatches()
    generateSpacyUnmatchedExplanations()

# temp
fakeJSON = [{"meget": "meget"}, {"fake": "fake"}]

#generateTXTfiles()
queryLabels()

def untrainSpacySolution():
    labelsDict = linkSpacyLabels()
    triples = createMagicUnfinished(labelsDict, fakeJSON)
    #print(triples)

def stringComparisonSolution():
    OntologyDict = queryLabels()
    

