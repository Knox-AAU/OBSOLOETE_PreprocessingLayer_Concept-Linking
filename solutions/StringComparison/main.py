from stringComparison import *
import json

input_file = "../../data/files/evaluationSet_EN.json"
output_file = "../../data/files/output.json"

f = open(input_file,  encoding="utf-8")
data = json.load(f)

def generateTXTfiles():
    generateOntologyClasses()
    generateOntologyDatatypes()

def stringComparisonSolution():
    ontTypes = queryLabels()
    triples = generateTriples(data, ontTypes)
    # Convert the array to a JSON string
    writeFile(output_file, json.dumps(triples))


if __name__=='__main__':
    stringComparisonSolution()

