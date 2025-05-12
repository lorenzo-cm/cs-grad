import numpy as np
import cv2
import glob

from .char_extraction import extract_characters

def get_train_data():
    train_image_files = sorted(glob.glob('./dados/treinamento/*.jpg'))
    train_character_images = [cv2.imread(img, cv2.IMREAD_GRAYSCALE) for img in train_image_files]

    train_label_files = sorted(glob.glob('./dados/labels10k/*.txt'))[:8000]
    train_labels = [open(label_file).read().strip() for label_file in train_label_files]

    X_train = []
    y_train = []

    for image, label in zip(train_character_images, train_labels):
        characters = extract_characters(image,
                                width=25,
                                overlap=2,
                                space_between=5,
                                initial_space=10)
        
        for char_image, char_label in zip(characters, label):
            X_train.append(char_image)
            y_train.append(char_label)

    X_train = np.array(X_train)
    y_train = np.array(y_train)
    
    return X_train, y_train


def get_test_data():
    test_image_files = sorted(glob.glob('./dados/teste/*.jpg'))
    test_character_images = [cv2.imread(img, cv2.IMREAD_GRAYSCALE) for img in test_image_files]

    test_label_files = sorted(glob.glob('./dados/labels10k/*.txt'))[9000:]
    test_labels = [open(label_file).read().strip() for label_file in test_label_files]

    X_test = []
    y_test = []

    for image, label in zip(test_character_images, test_labels):
        characters = extract_characters(image,
                                width=25,
                                overlap=2,
                                space_between=5,
                                initial_space=10)
        
        for char_image, char_label in zip(characters, label):
            X_test.append(char_image)
            y_test.append(char_label)

    X_test = np.array(X_test)
    y_test = np.array(y_test)
    
    return X_test, y_test


def get_valid_data():
    valid_image_files = sorted(glob.glob('./dados/validacao/*.jpg'))
    valid_character_images = [cv2.imread(img, cv2.IMREAD_GRAYSCALE) for img in valid_image_files]

    valid_label_files = sorted(glob.glob('./dados/labels10k/*.txt'))[8000:9000]
    valid_labels = [open(label_file).read().strip() for label_file in valid_label_files]

    X_valid = []
    y_valid = []

    for image, label in zip(valid_character_images, valid_labels):
        characters = extract_characters(image,
                                width=25,
                                overlap=2,
                                space_between=5,
                                initial_space=10)
        
        for char_image, char_label in zip(characters, label):
            X_valid.append(char_image)
            y_valid.append(char_label)

    X_valid = np.array(X_valid)
    y_valid = np.array(y_valid)
    
    return X_valid, y_valid