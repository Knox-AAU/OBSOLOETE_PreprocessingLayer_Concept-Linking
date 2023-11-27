import torch
import torch.nn as nn
import torch.optim as optim

class EntityLinkingModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(EntityLinkingModel, self).__init__()
        self.hidden_size = hidden_size
        self.embedding = nn.Embedding(input_size, hidden_size)
        self.gru = nn.GRU(hidden_size, hidden_size)
        self.fc = nn.Linear(hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, input_seq):
        embedded = self.embedding(input_seq)
        output, hidden = self.gru(embedded)
        output = self.fc(output[:, -1, :])
        output = self.softmax(output)
        return output


input_size = 1000
hidden_size = 256
output_size = 10

input_data = torch.randint(0, input_size, (100, 20))  # Example input data tensor
target_data = torch.randint(0, output_size, (100,))   # Example target labels tensor

model = EntityLinkingModel(input_size, hidden_size, output_size)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)


epochs = 10
for epoch in range(epochs):
    optimizer.zero_grad()
    output = model(input_data)
    loss = criterion(output, target_data)
    loss.backward()
    optimizer.step()


    print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss.item()}")


torch.save(model.state_dict(), 'entity_linking_model.pth')
