import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import os

from .model import CaptchaClassifier, CaptchaClassifierBigger
from .dataset import TrainDataset, ValidDataset, TestDataset
from .train import train_model
from .evaluate import evaluate_model

model = CaptchaClassifierBigger()

train_dataset = TrainDataset()
valid_dataset = ValidDataset()
test_dataset = TestDataset()

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
valid_loader = DataLoader(valid_dataset, batch_size=32, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)


trained_model = train_model(model, train_loader, valid_loader, criterion, optimizer, num_epochs=25, patience=5)

os.makedirs('models', exist_ok=True)
model_save_path = "models/nn_model_bigger.pth"
torch.save(trained_model.state_dict(), model_save_path)

evaluate_model(trained_model, test_loader, criterion)