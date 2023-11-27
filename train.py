import torch
import torch.nn as nn
import torch.optim as optim
import json
from torch.utils.data import DataLoader
from models.entity_linking_model import EntityLinkingModel
from data.enitity_linking_dataset import EntitylinkingDataset


def train(model, train_loader, val_loader, criterion, optimizer, num_epochs):
    for epoch in range(num_epochs):
        # Training loop
        model.train()
        total_loss = 0.0
        for inputs, targets in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        # Calculate average training loss for the epoch
        train_loss = total_loss / len(train_loader)

        # Validation loop
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for inputs, targets in val_loader:
                outputs = model(inputs)
                val_loss += criterion(outputs, targets).item()

        # Calculate average validation loss for the epoch
        val_loss /= len(val_loader)

        # Print training and validation loss for the epoch
        print(f"Epoch [{epoch + 1}/{num_epochs}] - Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")

        # Save model checkpoint if needed
        # Example: Save model every few epochs
        if (epoch + 1) % 5 == 0:
            torch.save(model.state_dict(), f"entity_linking_model_epoch_{epoch + 1}.pth")


# Example usage
if __name__ == "__main__":
    input_size = 1000
    hidden_size = 256
    output_size = 10
    learning_rate = 0.001
    num_epochs = 20

    model = EntityLinkingModel(input_size, hidden_size, output_size)
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    criterion = nn.CrossEntropyLoss()

# Example usage
if __name__ == "__main__":

    input_size = 1000
    hidden_size = 256
    output_size = 10
    learning_rate = 0.001
    num_epochs = 20


    model = EntityLinkingModel(input_size, hidden_size, output_size)
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    criterion = nn.CrossEntropyLoss()


def train(model, train_loader, val_loader, criterion, optimizer, num_epochs):
    for epoch in range(num_epochs):
        # Training loop
        model.train()
        total_loss = 0.0
        for inputs, targets in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()


        train_loss = total_loss / len(train_loader)


        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for inputs, targets in val_loader:
                outputs = model(inputs)
                val_loss += criterion(outputs, targets).item()


        val_loss /= len(val_loader)


        print(f"Epoch [{epoch+1}/{num_epochs}] - Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")



        if (epoch + 1) % 5 == 0:
            torch.save(model.state_dict(), f"entity_linking_model_epoch_{epoch+1}.pth")


if __name__ == "__main__":

    input_size = 1000
    hidden_size = 256
    output_size = 10
    learning_rate = 0.001
    num_epochs = 20

    # Initialize your model and optimizer
    model = EntityLinkingModel(input_size, hidden_size, output_size)
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    criterion = nn.CrossEntropyLoss()

    train_dataset = EntitylinkingDataset(data='data/exampleEntitys.json', train=True)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

    # For validation dataset
    val_dataset = EntitylinkingDataset(data='data/evaluationSet.json', train=False)
    val_loader = DataLoader(val_dataset, batch_size=32)