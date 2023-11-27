from rdflib import Graph, Namespace, RDF, RDFS

def parse_ontology(ontology_file_path):
    g = Graph()
    g.parse(ontology_file_path, format="ttl")

    dbpedia = Namespace("http://dbpedia.org/ontology/")  # Adjust based on your ontology's namespace

    classes = []
    properties = []

    # Extract classes
    for class_uri in g.subjects(RDF.type, RDFS.Class):
        if class_uri.startswith(dbpedia):
            classes.append(class_uri)

    # Extract properties
    for prop_uri in g.subjects(RDF.type, RDF.Property):
        if prop_uri.startswith(dbpedia):
            properties.append(prop_uri)

    return classes, properties


ontology_file_path = "data/ontology--DEV_type=parsed.ttl"
class_list, property_list = parse_ontology(ontology_file_path)
print("Classes:", class_list)
print("Properties:", property_list)

