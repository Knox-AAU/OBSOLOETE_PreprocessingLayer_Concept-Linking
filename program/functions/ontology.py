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
        searchLanguage = "en"
        for sentence in object['sentences']:
            sent = sentence['sentence']
            ems = sentence['entityMentions']

            print(sentence['sentence'])
            new_sent = sent

            ems_indices = []
            for em in ems:
                ems_indices.append((em['startIndex'], em['endIndex']))

            #sletter de ord i sætningen, der er EMs
            for start_index, end_index in reversed(ems_indices):
                new_sent = new_sent[:start_index] + new_sent[end_index+2:]
            
            new_sent = new_sent.removesuffix(".")
            words = new_sent.split(" ")

            #words der findes i ontologyen
            matchingWords = []

            for class_name, labels_list in classesDict.items():
                for label_dict in labels_list:
                    # Check if the search language is in the label_dict
                    if searchLanguage in label_dict:
                        label = label_dict[searchLanguage]
                        for word in words:
                            if word.lower() in label.lower():
                                matchingWords.append({class_name: label})
                    else:
                        # If the search language is not found, try translating the word and check in English labels
                        for word in words:
                            translated_word = translateWordToEn(word, language)
                            if translated_word.lower() in label_dict.get('en', '').lower():
                                matchingWords.append({class_name: label_dict.get('en', '')})
            
            #opdatér passende IRI-domain, når vi har snakket med gruppe C
            for word in matchingWords:
                for em in ems:
                    triples.append((em['iri'], "rdfs:type/is_a", "http://dbpedia.org/ontology/" + word))
    return triples
    
    

""" #Vi's translate funktion kommer her
            if lang != 'en':
                for word in words:
                    word = translate(word)
            
            #Opdatér til at søge på labels(values) - ikke classes(keys)
            for word in words:
                if word.capitalize() in dict:
                    typeWords.append(word) """
