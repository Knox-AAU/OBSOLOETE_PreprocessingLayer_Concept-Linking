import torch
import json
from torch.utils.data import DataLoader
from data.enitity_linking_dataset import EntitylinkingDataset
from models.entity_linking_model import EntityLinkingModel


def make_predictions(model, data_loader):
    #predictions = []
    #model.eval()
    #with torch.no_grad():
    #    for inputs, _ in data_loader:
    #        outputs = model(inputs)
    #        _, predicted = torch.max(outputs, 1)
    #        predictions.extend(predicted.tolist())
    #return predictions

    predictions = []
    model.eval()
    with torch.no_grad():
        for input_data, target_data in data_loader:
            outputs = model(input_data)
            _, predicted = torch.max(outputs, 1)
            predictions.extend(predicted.tolist())

    return predictions


input_size = 1000
hidden_size = 256
output_size = 10

model_path = 'entity_linking_model.pth'
model = EntityLinkingModel(input_size, hidden_size, output_size)  # Initialize model
model.load_state_dict(torch.load(model_path))
model.eval()

# Load entity mentions from the ExampleEntity.json file
with open('data/Input.json', 'r') as json_file:
    entity_mentions_data = json.load(json_file)

# Create a dataset from the loaded entity mentions
entity_mentions_dataset = EntitylinkingDataset(data=entity_mentions_data, train=True)
entity_mentions_loader = DataLoader(entity_mentions_dataset, batch_size=32, collate_fn=entity_mentions_dataset.custom_collate_fn)

# Make predictions using the loaded model and entity mentions
predicted_indices = make_predictions(model, entity_mentions_loader)

# Map predicted indices to triples (use the same logic as in the previous example)
# Example ontology_mapping
ontology_mapping = {
    0: ('knox-kb01.srv.aau.dk/Barack_Obama', 'rdf:type', 'http://dbpedia.org/ontology/Person'),
    1: ('knox-kb01.srv.aau.dk/Michele_Obama', 'rdf:type', 'http://dbpedia.org/ontology/PersonFunction')
    # Add more mappings as needed
}

# Generate triples from predicted indices using the ontology mapping
resulting_triples = []
for idx in predicted_indices:
    if idx in ontology_mapping:
        resulting_triples.append(ontology_mapping[idx])

# Write triples to a JSON file
output_file_path = 'predicted_output_triples.json'
with open(output_file_path, 'w') as output_file:
    json.dump(resulting_triples, output_file, indent=4)

print(f"Predicted triples written to {output_file_path}")

predicted_indices = make_predictions(model, entity_mentions_loader)
