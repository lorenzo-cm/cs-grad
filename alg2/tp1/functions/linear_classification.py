from functions.utils import timer
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

@timer
def linear_classification(X, y, a, b, class1, class2, recursive=False, plot=False):
    
    equation = lambda x: a*x + b
    labels = []
    TP, TN, FP, FN = 0, 0, 0, 0
    true_positives, true_negatives, false_positives, false_negatives = [], [], [], []

    for i, (x1, x2) in enumerate(X):
        if x2 >= equation(x1):
            labels.append(class1)
        else:
            labels.append(class2)

        if labels[i] == y[i] and labels[i] == class1:
            TP += 1
            true_positives.append((x1, x2))
        elif labels[i] == y[i] and labels[i] == class2:
            TN += 1
            true_negatives.append((x1, x2))
        elif labels[i] != y[i] and labels[i] == class1:
            FP += 1
            false_positives.append((x1, x2))
        else:
            FN += 1
            false_negatives.append((x1, x2))

    accuracy = (TP + TN) / (TP + TN + FP + FN)

    if accuracy <= 0.5 and not recursive:
        return linear_classification(X, y, a, b, class2, class1, recursive=True, use_timer=False)

    precision = TP / (TP + FP) if (TP + FP) != 0 else 0
    recall = TP / (TP + FN) if (TP + FN) != 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0

    # plot the data
    # Convert data to a DataFrame for Seaborn
    data = []
    for x, label in zip(X, labels):
        actual = y[np.where(X == x)[0][0]]
        data.append([x[0], x[1], "True Positive" if label == class1 and actual == class1 else 
                    "True Negative" if label == class2 and actual == class2 else
                    "False Positive" if label == class1 and actual == class2 else
                    "False Negative"])
    df = pd.DataFrame(data, columns=['X1', 'X2', 'Type'])
    
    # Set Seaborn style
    sns.set_style("whitegrid")
    palette = {
        "True Positive": "green", 
        "True Negative": "red", 
        "False Positive": "blue", 
        "False Negative": "yellow"
    }

    # Plot
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='X1', y='X2', hue='Type', palette=palette, s=100)
    
    # Plotting the decision boundary
    x_vals = np.linspace(min(X[:,0]), max(X[:,0]), 100)
    plt.plot(x_vals, equation(x_vals), '-r', label='Decision Boundary')
    
    plt.title('Linear Classification with Seaborn')
    plt.legend()
    plt.show()

    return accuracy, precision, recall, f1_score
