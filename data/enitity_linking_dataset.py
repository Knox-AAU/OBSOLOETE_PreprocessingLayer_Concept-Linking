import torch
import json
import spacy
from torch.utils.data import Dataset


class EntitylinkingDataset(Dataset):
    def __init__(self, data, train=True):
        self.data = data
        self.train = train
        self.token_to_index = {}
        self.nlp = spacy.load("en_core_web_sm")
        self.populate_token_to_index()

    def populate_token_to_index(self):
        all_tokens = [...]  # Replace [...] with the actual tokens you have
        unique_tokens = set(all_tokens)
        # Add <UNK> token to the token_to_index dictionary
        unique_tokens.add('<UNK>')
        self.token_to_index = {token: idx for idx, token in enumerate(unique_tokens)}

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]

        input_data = self.process_data(item)
        target_data = self.process_target(item)

        return input_data, target_data

    def load_data(self, data_path):
        with open(data_path, 'r') as file:
            data = json.load(file)
        return data

    def process_data(self, item, max_length=50):
        print(item.keys())  # Print keys to understand the structure

        # Extracting sentence from the 'sentences' field of the item
        sentence_info = item.get('sentences', [{}])[0]
        sentence_text = sentence_info.get('sentence', '')

        if sentence_text:
            # Tokenize the sentence using spaCy
            tokens = [token.text for token in self.nlp(sentence_text)]

            # Pad tokens to a fixed length
            if len(tokens) < max_length:
                tokens += ['<PAD>'] * (max_length - len(tokens))
            else:
                tokens = tokens[:max_length]

            # Convert tokens to indexes using the token_to_index mapping
            indexed_tokens = [self.token_to_index.get(token, self.token_to_index['<UNK>']) for token in tokens]
            input_data = torch.tensor(indexed_tokens)  # Convert to PyTorch tensor
        else:
            # Handle cases where 'sentence' key is missing or empty
            print("No 'sentence' key found or it's empty in the item:", item)
            input_data = torch.zeros(max_length, dtype=torch.long)  # Padding with zeros or handle accordingly

        return input_data



    def one_hot_encode(self, entity_string):
        print(entity_string)  # Add this line to inspect the entity string
        index = self.token_to_index.get(entity_string, -1)
        if index != -1:
            one_hot = [0] * len(self.token_to_index)
            one_hot[index] = 1
            return one_hot
        else:
            return [0] * len(self.token_to_index)

    def process_target(self, item):
        entity_mentions = item.get('sentences', [{}])[0].get('entityMentions', [])
        target_data = [entity['type'] for entity in entity_mentions]

        # Convert target_data to tensors using the one_hot_encode method
        target_tensor_data = [torch.tensor(self.one_hot_encode(entity), dtype=torch.float32) for entity in target_data]

        return target_tensor_data

    def custom_collate_fn(self, batch):
        batch = sorted(batch, key=lambda x: len(x[0]), reverse=True)
        max_length_input = max(len(x[0]) for x in batch)
        max_length_target = max(len(x[1]) for x in batch)

        padded_input_data = [torch.cat([x[0], torch.zeros(max_length_input - len(x[0]), dtype=torch.long)]) for x in
                             batch]
        padded_input_data = torch.stack(padded_input_data, dim=0)

        # Convert target data (which is a list of tensors) into a tensor of tensors
        padded_target_data = [torch.cat([t, torch.zeros(max_length_target - len(t), dtype=torch.long)]) for x in batch
                              for t in x[1]]
        padded_target_data = torch.stack(padded_target_data, dim=0)

        return padded_input_data, padded_target_data
