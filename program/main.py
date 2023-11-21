from functions.ontology import *
from functions.spacy import *
import json

f = open("../files/test.JSON")
data = json.load(f)

def generateTXTfiles():
    generateOntologyClasses()
    generateOntologyDatatypes()
    generateSpacyLabels()
    generateSpacyMatches()
    generateSpacyUnmatchedExplanations()
#generateOntologyClasses()
#generateOntologyDatatypes()

#generateTXTfiles()

def untrainedSpacySolution():
    labelsDict = linkSpacyLabels()
    triples = createMagicUnfinished(labelsDict, data)
    print(*triples, sep="\n")
#untrainedSpacySolution()

def stringComparisonSolution():
    ontTypes = queryLabels()
    triples = generateTriples(data, ontTypes)
    # Convert the array to a JSON string
    writeFile("../files/output.json", json.dumps(triples))

    
        
stringComparisonSolution()