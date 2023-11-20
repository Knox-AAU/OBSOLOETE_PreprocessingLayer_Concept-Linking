from functions.ontology import *
from functions.untrainedSpacy import *
import json

f = open("../files/test.JSON")
data = json.load(f)

def generateTXTfiles():
    generateOntologyClasses()
    generateSpacyLabels()
    generateSpacyMatches()
    generateSpacyUnmatchedExplanations()


#generateTXTfiles()

def untrainSpacySolution():
    labelsDict = linkSpacyLabels()
    triples = createMagicUnfinished(labelsDict, data)
    print(*triples, sep="\n")
untrainSpacySolution()

def stringComparisonSolution():
    ontTypes = queryLabels()
    triples = generateTriples(data, ontTypes)
    print(*triples, sep="\n")
#stringComparisonSolution()
