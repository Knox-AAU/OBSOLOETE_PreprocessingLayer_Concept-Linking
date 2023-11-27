from rdflib import Graph

def parse_ttl(file_path):
    g = Graph()
    g.parse(file_path, format="ttl")

    query = """
    SELECT ?datatype ?label
    WHERE {
        ?datatype a <http://www.w3.org/2000/01/rdf-schema#Datatype> .
        ?datatype <http://www.w3.org/2000/01/rdf-schema#label> ?label .
    }
    """

    results = g.query(query)

    datatype_info = {}
    for row in results:
        datatype_info[str(row['datatype'])] = str(row['label'])

    return datatype_info

ontology_file_path = "data/ontology--DEV_type=parsed.ttl"
datatypes = parse_ttl(ontology_file_path)
print(datatypes)