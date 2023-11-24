from functions.ontology import *
from functions.untrainedSpacy import *
import json

f = open("../files/entity_mentions.json",  encoding="utf-8")
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
    triples = generateTriplesFromJSON(labelsDict, data)
    
    output_path = "../files/output.json"
    with open(output_path, "w", encoding = "utf-8") as outfile:
        json.dump(triples, outfile, ensure_ascii=False, indent=4)

    #writeFile("../files/output.json", json.dumps(triples))

untrainedSpacySolution()

def stringComparisonSolution():
    ontTypes = queryLabels()
    triples = generateTriples(data, ontTypes)
    # Convert the array to a JSON string
    writeFile("../files/output.json", json.dumps(triples))


g = Graph()
g.parse("files/ontology.ttl", format="ttl")

# TODO: Get all datatype properties from ontology.
query = '''
PREFIX dbo: <http://dbpedia.org/ontology/>

SELECT DISTINCT ?exampleValue
WHERE {
  ?resource dbo:area ?exampleValue .
  FILTER(isLiteral(?exampleValue))
}
LIMIT 10
'''
result = g.query(query)
for row in result:
    print(row)
        
#stringComparisonSolution()