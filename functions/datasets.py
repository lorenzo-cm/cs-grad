import numpy as np
import pandas as pd

from sklearn.datasets import load_iris, load_wine, load_digits, load_breast_cancer, load_linnerud, load_diabetes, fetch_california_housing

def load_iris_():
    data = load_iris()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['target'] = data.target
    return df

def load_wine_():
    data = load_wine()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['target'] = data.target
    return df

def load_digits_():
    data = load_digits()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['target'] = data.target
    return df

def load_breast_cancer_():
    data = load_breast_cancer()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['target'] = data.target
    return df

def load_linnerud_():
    """1 if weight of the person is above the average of the dataset, 0 otherwise"""
    data = load_linnerud()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['target'] = pd.DataFrame(data.target[:,0], columns=[data.target_names[0]])
    df['target'] = np.where(df['target'] > 178.6, 1, 0)
    return df

def load_diabetes_():
    """1 if the patient's disease progressed, 0 otherwise"""
    data = load_diabetes()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['target'] = data.target
    df['target'] = np.where(df['target'] > 200, 1, 0)
    return df

def load_california_housing_():
    data = fetch_california_housing()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['target'] = data.target
    df['target'] = df['target'].apply(lambda x: 1 if x > 2.068 else 0)
    return df

def load_mobile():
    """1 if the mobile has bluetooth, 0 otherwise"""
    df = pd.read_csv('data/mobile.csv')
    df = df.rename(columns={'blue': 'target'})
    return df

def load_diabetes2():
    """1 If the patient has diabetes, 0 otherwise"""
    df = pd.read_csv('data/diabetes.csv')
    df = df.rename(columns={'diabetes': 'target'})
    df['gender'] = df['gender'].apply(lambda x: 1 if x == 'Female' else 0)
    df['smoking_history'] = df['smoking_history'].apply(lambda x: 0 if x == 'never' else 4 if x == 'No Info' else 5 if x == 'ever' else 8 if x == 'former' else 8 if x == 'not current' else 10)
    return df

def load_pokemon():
    df = pd.read_csv('data/pokemon.csv')
    df = df.drop(['#', 'Name', 'Type 2', 'Generation', 'Legendary'], axis=1)
    df = df.rename(columns={'Type 1': 'target'})
    unique_classes = np.unique(df['target'])

    type_to_number = {}
    for type in unique_classes:
        type_to_number[type] = len(type_to_number)
    type_to_number

    df['target'] =  df['target'].apply(lambda x: type_to_number[x])
    return df


datasets = {
    "iris": load_iris_,
    "wine": load_wine_,
    "digits": load_digits_,
    "breast_cancer": load_breast_cancer_,
    "linnerud": load_linnerud_,
    "diabetes": load_diabetes_,
    "california_housing": load_california_housing_,
    "mobile": load_mobile,
    "diabetes2": load_diabetes2,
    "pokemon": load_pokemon
}


