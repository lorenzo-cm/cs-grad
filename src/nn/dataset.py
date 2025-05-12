from torch.utils.data import Dataset
from ..utils.load_data import get_train_data, get_valid_data, get_test_data
from ..utils.char_to_int import convert_char_to_int
from torchvision import transforms

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

class TrainDataset(Dataset):
    def __init__(self):
        self.X_train, self.y_train = get_train_data()
        self.y_train = [convert_char_to_int(label) for label in self.y_train]
        
        # Filter out entries where label is 36
        self.X_train, self.y_train = zip(*[(x, y) for x, y in zip(self.X_train, self.y_train) if y != 36])
        
        self.transform = transform

    def __len__(self):
        return len(self.X_train)

    def __getitem__(self, idx):
        image = self.X_train[idx]
        label = self.y_train[idx]
        
        image = self.transform(image)
        
        return image, label

class ValidDataset(Dataset):
    def __init__(self):
        self.X_valid, self.y_valid = get_valid_data()
        self.y_valid = [convert_char_to_int(label) for label in self.y_valid]
        
        # Filter out entries where label is 36
        self.X_valid, self.y_valid = zip(*[(x, y) for x, y in zip(self.X_valid, self.y_valid) if y != 36])
        
        self.transform = transform

    def __len__(self):
        return len(self.X_valid)

    def __getitem__(self, idx):
        image = self.X_valid[idx]
        label = self.y_valid[idx]
        
        image = self.transform(image)
        
        return image, label

class TestDataset(Dataset):
    def __init__(self):
        self.X_test, self.y_test = get_test_data()
        self.y_test = [convert_char_to_int(label) for label in self.y_test]
        
        # Filter out entries where label is 36
        self.X_test, self.y_test = zip(*[(x, y) for x, y in zip(self.X_test, self.y_test) if y != 36])
        
        self.transform = transform

    def __len__(self):
        return len(self.X_test)

    def __getitem__(self, idx):
        image = self.X_test[idx]
        label = self.y_test[idx]
        
        image = self.transform(image)
        
        return image, label
