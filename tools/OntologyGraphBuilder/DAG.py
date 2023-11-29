import networkx as nx
import matplotlib.pyplot as plt
from rdflib import Graph, URIRef
from rdflib.plugins.sparql import prepareQuery

def build_dag():
    graph = build_ontology_graph(extract_classes_from_ontology())
    root_class_name = "StatedResolution"
    try:
        subgraph = depth_first_traversal(graph, root_class_name)
        visualize_graph(subgraph)
    except Exception as e:
        print(f'An error occurred {e}')

def build_ontology_graph(ontology_data):
    graph = nx.DiGraph()
    for parent, child in ontology_data:
        graph.add_edge(child, parent)
    return graph

def find_node_without_parents(graph):
    in_degrees = dict(graph.in_degree())
    for node, in_degree in in_degrees.items():
        if in_degree == 0:
            return node
    return None


def visualize_graph(graph):
    fig = plt.figure(figsize=(10, 8), dpi=600)
    pos = nx.spring_layout(graph, k=0.2)

    start_node = find_node_without_parents(graph)
    node_colors = ['orange' if node == start_node else 'skyblue' for node in graph.nodes]

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color=node_colors,
        font_size=1,  # Adjust the font size as needed
        font_color="black",
        font_weight="bold",
        edge_color="gray",
        linewidths=0.5,
        arrowsize=10,
        node_size=50,  # Adjust the node size as needed
    )

    plt.title("Ontology Graph")
    plt.show()
    fig.clf()
    plt.close(fig)
def depth_first_traversal(graph, start_node):
    visited_up = set()
    visited_down = set()
    sub_graph = nx.DiGraph()

    def dfs_up(node):
        if node not in visited_up:
            visited_up.add(node)
            for parent in graph.predecessors(node):
                sub_graph.add_edge(parent, node)
                dfs_up(parent)

    def dfs_down(node):
        if node not in visited_down:
            visited_down.add(node)
            for child in graph.successors(node):
                sub_graph.add_edge(node, child)
                dfs_down(child)

    dfs_up(start_node)
    dfs_down(start_node)
    return sub_graph



def extract_classes_from_ontology():
    g = Graph()
    g.parse("../files/ontology.ttl", format="ttl")

    # Define RDF namespace prefixes
    rdfs = URIRef("http://www.w3.org/2000/01/rdf-schema#")
    owl = URIRef("http://www.w3.org/2002/07/owl#")

    query_str = """SELECT ?class ?subclass
    WHERE {
        ?class a owl:Class .

        OPTIONAL {
            ?class rdfs:subClassOf ?subclass.
        }
    }"""
    query = prepareQuery(query_str, initNs={"rdfs": rdfs, "owl": owl})
    res = g.query(query)
    entries = []

    try:
        for row in res:
            class_uri = row['class']
            class_name = class_uri.split("/")[-1]
            subclass = row['subclass']
            if subclass is not None:
                entry = (class_name, subclass.split("/")[-1])
            else:
                entry = (class_name, None)
            if entry not in entries:
                entries.append(entry)
    except Exception as e:
        print(e)

    return entries