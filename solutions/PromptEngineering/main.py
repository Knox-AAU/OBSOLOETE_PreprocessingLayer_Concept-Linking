import json
import re
import time

from llama_cpp import Llama

LLM = Llama(model_path="C:/Users/lucas/GitRepos/Llama_2/llama.cpp/models/7B/ggml-model-q4_0.bin", n_ctx=32768)

# Read all ontology classes from file
def read_ontology_class():
    with open('../files/person.txt') as file:
        return [line.strip() for line in file]

# Open the JSON file with sentences for reading - use as input
with open('../files/sentence.json', 'r') as file:
    data = json.load(file)

# Generates the respective triples of the right format
def generate_triples(output_data):
    triples = []
    for sentence_data in output_data["sentences"]:
        for mention in sentence_data["entityMentions"]:
            iri = mention["iri"]
            classification = mention["classification"]

            # Skip creating triples if the classification is "Unknown"
            if classification == "Unknown":
                continue

            # Map the classification to the corresponding DBpedia ontology type
            dbpedia_type = f"http://dbpedia.org/ontology/{classification}"

            triple = [iri, "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", dbpedia_type]
            triples.append(triple)

    return triples


ontology_classes = "Person, Place, Time, Organisation, Event, Academic, AcademicConference"

output_data = {"sentences": []}

max_retries = 3

# Iterate through each sentence
for sentence_data in data[0]["sentences"]:
    content_sentence = sentence_data["sentence"]

    # Iterate through each entity mention in the sentence
    for mention in sentence_data["entityMentions"]:
        if mention["type"] == "Entity":
            content_entity = mention["name"]

            prompt_template = (
                "##Context: \n"
                "The input sentence is all your knowledge. \n"
                "Do not answer if it can't be found in the sentence. \n"
                "Do not use bullet points. \n"
                "Given the input in the form of the content from a file: \n"
                "[Sentence]: {content_sentence} \n"
                "[EntityMention]: {content_entity} \n"
                "##Prompt: \n"
                f"Classify the entity in regards to ontology classes: {read_ontology_class()} \n"
                "The output answer must be in JSON in the following format: \n"
                "{{ \n"
                "'Entity': 'Eiffel Tower', \n"
                "'Class': 'ArchitecturalStructure' \n"
                "}} \n"
            )

            prompt = prompt_template.format(
                content_sentence=content_sentence,
                content_entity=content_entity,
                ontology_classes=ontology_classes,
            )

            print(prompt)

            retry_count = 0
            while retry_count < max_retries:
                output = LLM(prompt, max_tokens=10000)

                if output["choices"] and output["choices"][0]["text"] not in (None, '.'):
                    result_text = output["choices"][0]["text"]
                    break
                else:
                    print("Output is null, empty, or contains only a dot. Retrying...")
                    retry_count += 1
                    time.sleep(2)

            result_text = result_text.strip()

            match = re.search(r"'Class': ['\"](\w+)['\"]", result_text)
            classification = match.group(1) if match else "Unknown"

            output_sentence_data = {
                "sentence": content_sentence,
                "entityMentions": [
                    {
                        "name": mention["name"],
                        "startIndex": mention["startIndex"],
                        "endIndex": mention["endIndex"],
                        "iri": mention["iri"],
                        "classification": classification
                    }
                ]
            }

            output_data["sentences"].append(output_sentence_data)

            # Print the result for the current sentence
            print("Sentence:", content_sentence)
            print("Entity Mention:", content_entity)
            print("Classification:", classification)
            print(output["choices"][0]["text"])

# Specify the output file path
output_file_path = "output.json"

# Generate triples
triples = generate_triples(output_data)

# Specify the triples output file path
triples_file_path = "Triples.json"

# Save the triples to a JSON file
with open(triples_file_path, 'w') as triples_file:
    json.dump(triples, triples_file, indent=2)

# Save the result to a JSON file
with open(output_file_path, 'w') as output_file:
    json.dump(output_data, output_file, indent=2)

print("Output saved to:", output_file_path)

print("Triples saved to:", triples_file_path)


# f"Given the input in the form of the content from the file: {content}. \n"
# f"Classify the entities in regards to ontology classes: {read_ontology_class()} \n"
# f"The output answer should only be the name of the class matching the most. \n"
# f"Create a list of each entity mention and its classification. \n"
# f"The output must be in JSON format"


# f"##Context: \n"
# f"The data is all your knowledge. \n"
# f"Do not answer, if it can't be found in the data. \n"
# f"If so, respond in one sentence 'I can't answer that question'. \n"
# f"Do not use bullet points \n"
# f"##Prompt format: \n"
# f"data: \n"
# f"The given input: \n"
# f"For each [Sentence] in Sentences: {content_sentence} \n"
# f"And for each [EntityMention]: {content_entity}. \n"
# f"The ontology classes: {ontology_classes}. \n"
# f"Question: \n"
# f"Please classify the entity mentions from the sentences, \n"
# f"based on the ontology classes (Answer this based on data)."


# f"Given the input in the form of the content from the file: \n"
# f"[Sentences]: {content_sentence} \n"
# f"[EntityMention]: {content_entityMentions} \n"
# f"Classify the entities in regards to ontology classes: {ontology_classes} \n"
# f"The output answer should only be the name of the class matching the most. \n"
# f"Create a list of the used classes for each entity mention and its classification. \n"
# f"The output must be in JSON format"
