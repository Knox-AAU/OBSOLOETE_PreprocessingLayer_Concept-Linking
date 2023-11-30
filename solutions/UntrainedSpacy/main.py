from untrainedSpacy import *
import json

input_file = "../../data/files/evaluationSet_EN.json"
output_file = "../../data/files/output.json"

f = open(input_file,  encoding="utf-8")
data = json.load(f)

def generateTXTfiles():
    generateSpacyLabels()
    generateSpacyMatches()
    generateSpacyUnmatchedExplanations()

def untrainedSpacySolution():
    triples = generateTriplesFromJSON(data)
    
    with open(output_file, "w", encoding = "utf-8") as outfile:
        json.dump(triples, outfile, ensure_ascii=False, indent=4)

if __name__=='__main__':
    untrainedSpacySolution()