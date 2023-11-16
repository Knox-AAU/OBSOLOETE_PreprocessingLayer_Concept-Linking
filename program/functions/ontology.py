from .utils import *
from rdflib import Graph, URIRef, Namespace


def generateOntologyClasses():
    g = Graph()
    g.parse("files/ontology.ttl", format="ttl")

    # TODO: Get all correct classes from ontology.
    # se om ontology og spacy classerne er de samme, hvis nej print listen for dem
    query = """
        SELECT DISTINCT ?class
        WHERE {
            ?class a owl:Class .
        }
    """

    results = g.query(query)
    ontology_classes = [str(result["class"]) for result in results]

    # Collect ontology classes in array and sets it to lower case. Then saves to file.
    ontology_classesLC = []
    for ontology_class in ontology_classes:
        ontology_classesLC.append(
            ontology_class.removeprefix("http://dbpedia.org/ontology/").lower()
        )
    writeFile("../documents/ontology_classes.txt", "\n".join(ontology_classesLC))

def queryLabels():
    g = Graph()
    g.parse("files/ontology.ttl", format="ttl")

    qres = g.query( """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>

    SELECT ?class (lang(?label) as ?language) ?label
    WHERE {
        ?class a owl:Class .
        ?class rdfs:label ?label .
    } 
    """ )

    classesDict = {}
    for row in qres:
        r = str(row).split()

        #prov:Revision i ontology bliver til provRevision. Hvad er prov?
        className = "".join(c for c in r[0] if c.isalpha()).removeprefix("rdflibtermURIRefhttpdbpediaorgontology")
        labelLang = "".join(c for c in r[1] if c.isalpha()).removeprefix("rdflibtermLiteral")
        label = "".join(c for c in r[2] if c.isalpha()).removeprefix("rdflibtermLiteral")
        if className not in classesDict:
            classesDict[className] = []
        classesDict[className].append({labelLang: label})
    
    with open("../documents/ontology_CL.txt", 'w') as f:
       for key, value in classesDict.items():
          f.write(f'{key}: {value}\n')
    return classesDict

def generateTriples(JSONObject, classesDict):
    triples = []
    for object in JSONObject:
        language = object["language"]
        ontologyLanguage = "en"
        for sentence in object['sentences']:
            sent = sentence['sentence']
            ems = sentence['entityMentions']
            new_sent = sent

            ems_indices = []
            for em in ems:
                ems_indices.append((em['startIndex'], em['endIndex']))

            #sletter de ord i sætningen, der er EMs
            for start_index, end_index in reversed(ems_indices):
                new_sent = new_sent[:start_index] + new_sent[end_index+2:]
            
            new_sent = new_sent.removesuffix(".")
            words = new_sent.split(" ")

            matchingWords = [] #words der findes i ontologyen
            SIMILARITY_REQ = 0.9 #minimumkrav til string similarity.

            if language is ontologyLanguage:
                matchingWords = findEnMatches(words, classesDict, matchingWords, SIMILARITY_REQ)
            else:
                matchingWords = findNonEnMatches(words, classesDict, matchingWords, SIMILARITY_REQ, language)
 
            #HUSK opdatér passende IRI-domain for predicate, når vi har snakket med gruppe C
            for word in matchingWords:
                for em in ems:
                    triples.append((em['iri'], "rdfs:type/is_a", "http://dbpedia.org/ontology/" + word['className']))
    return triples

# For hvert ord, check om det matcher et engelsk label på een af vores dict classer med minimin SIMILARITY_REQ. Hvis ja, tilføj til matchingWords.
def findEnMatches(words, classesDict, matchingWords, SIMILARITY_REQ):
    for word in words:
                for className, labelsList in classesDict.items():
                    for label_dict in labelsList:
                        if 'en' in label_dict and similar(word.lower(), label_dict['en'].lower()) >= SIMILARITY_REQ:
                            matchingWords.append({'className': className, 'label': word})
                            break
    return matchingWords

# Samme som findEnMatches, men tjekker efter et label match på originalsproget. Hvis der ikke findes et label på sproget, så oversætter vi og leder efter et passende engelsk label.
def findNonEnMatches(words, classesDict, matchingWords, SIMILARITY_REQ, language):
    translatedWords = []
    for word in words:
        translatedWords.append(translateWordToEn(word, language))

    for i, word in enumerate(words):
                for className, labelsList in classesDict.items():
                    for label_dict in labelsList:
                        if language in label_dict and similar(word.lower(), label_dict[language].lower()) >= SIMILARITY_REQ:
                            matchingWords.append({'className': className, 'label': word})
                            break  
                        elif 'en' in label_dict and similar(translatedWords[i].lower(), label_dict['en'].lower()) >= SIMILARITY_REQ:
                            matchingWords.append({'className': className, 'label': word})
                            break
    return matchingWords