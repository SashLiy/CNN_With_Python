# -*- coding: utf-8 -*-
"""Building a CNN with Python.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tFxXNMRzOY8IaLrqjDujUzUdYrGqQB0j

# Building a Convolutional Neural Network (CNN) with PyTorch
### From medium article - https://medium.com/@parktwin2/building-a-convolutional-neural-network-cnn-with-pytorch-bdd3c5fe47cb

### 1. install pyTorch and deep learning libraries
"""

# Install PyTorch
!pip install torch torchvision

# Import PyTorch
import torch
import torchvision
import torchvision.transforms as transforms

"""### 2. Data Preperation and Loading"""

# Download and load CIFAR-10 dataset
transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                        download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=4,
                                          shuffle=True, num_workers=2)

"""### 3. creating a CNN architecture"""

import torch.nn as nn
import torch.nn.functional as F

# Define a simple CNN architecture
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        # Convolutional layer 1 with 3 input channels (for RGB images), 6 output channels, and 5x5 kernel
        self.conv1 = nn.Conv2d(3, 6, 5)
        # Max pooling layer with a 2x2 window
        self.pool = nn.MaxPool2d(2, 2)
        # Convolutional layer 2 with 6 input channels (from the previous layer), 16 output channels, and 5x5 kernel
        self.conv2 = nn.Conv2d(6, 16, 5)
        # Fully connected layers
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 20)
        self.fc3 = nn.Linear(20, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

"""### 4. Training CNN"""

dataset  = trainset

# Initialize your CNN model
cnn = Net()
# Define loss function and optimizer
criterion = nn.CrossEntropyLoss()  # Cross-entropy loss for classification
optimizer = torch.optim.SGD(cnn.parameters(), lr=0.001, momentum=0.9)  # Stochastic Gradient Descent optimizer
# Split your data into training and validation sets
train_size = int(0.8 * len(dataset))
train_set, val_set = torch.utils.data.random_split(dataset, [train_size, len(dataset) - train_size])
train_loader = torch.utils.data.DataLoader(train_set, batch_size=4, shuffle=True)
val_loader = torch.utils.data.DataLoader(val_set, batch_size=4, shuffle=False)
# Training loop
num_epochs = 10
for epoch in range(num_epochs):
    running_loss = 0.0
    for i, data in enumerate(train_loader, 0):
        inputs, labels = data
        optimizer.zero_grad()  # Zero the parameter gradients to avoid accumulation
        outputs = cnn(inputs)  # Forward pass
        loss = criterion(outputs, labels)  # Compute the loss
        loss.backward()  # Backpropagation
        optimizer.step()  # Update the model parameters
print('Finished Training')

"""### 5. Evaluating the model"""

correct = 0
total = 0
# Set the model to evaluation mode
cnn.eval()
with torch.no_grad():
    for data in val_loader:
        images, labels = data
        outputs = cnn(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
print(f'Accuracy on the validation set: {100 * correct / total:.2f}%')

"""### 6. Fine tuning a pre trained model"""

import torch
import torch.nn as nn
import torchvision
from torchvision import transforms, datasets

# Load a pre-trained ResNet-18 model
model = torchvision.models.resnet18(pretrained=True)

# Freeze all layers except the final classification layer
for param in model.parameters():
    param.requires_grad = False
model.fc.requires_grad = True

# Modify the final classification layer for the number of classes in your dataset
num_classes = 10  # Example: 10 classes
model.fc = nn.Linear(model.fc.in_features, num_classes)

# Define the loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.fc.parameters(), lr=0.001, momentum=0.9)

# Data loading and training loop (similar to the previous section)
# ...

# Continue with validation and evaluation (similar to the previous section)
# ...

"""### 7. Transfer learning"""

import torch
import torch.nn as nn
import torchvision
from torchvision import transforms, datasets

# Load a pre-trained ResNet-18 model
model = torchvision.models.resnet18(pretrained=True)
model = nn.Sequential(*list(model.children())[:-1])  # Remove the last classification layer

# Define a new classifier to use the extracted features
classifier = nn.Sequential(
    nn.Linear(512, 256),  # The number of input features depends on the pre-trained model
    nn.ReLU(),
    nn.Linear(256, num_classes),  # Output layer for your specific task
)

# Combine the feature extractor and the new classifier
transfer_model = nn.Sequential(model, classifier)

# Define the loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(transfer_model.parameters(), lr=0.001, momentum=0.9)

# Data loading and training loop (similar to the previous sections)
# ...

# Continue with validation and evaluation (similar to the previous sections)
# ...

"""### 8. Saving the trained model"""

# Save the trained model
torch.save(cnn.state_dict(), 'trained_model.pth')

"""### 9. loading the trained model for inference"""

# Load the trained model
model = Net()
model.load_state_dict(torch.load('trained_model.pth'))
model.eval()

"""### 10. Preprocessing new images"""

from torchvision import transforms
from PIL import Image

# Load and preprocess a new image
transform = transforms.Compose([
    transforms.Resize((32, 32)),  # Resize the image to match the model's input size
    transforms.ToTensor(),  # Convert the image to a PyTorch tensor
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalize the image
])
image_path = '/content/kdu logo.jpeg'
image = Image.open(image_path)
input_tensor = transform(image)
input_tensor = input_tensor.unsqueeze(0)  # Add a batch dimension

"""### 11. Making predictions"""

# Perform inference on the preprocessed image
with torch.no_grad():
    output = model(input_tensor)
    _, predicted_class = output.max(1)

# Print the predicted class
print(f'Predicted class: {predicted_class.item()}')