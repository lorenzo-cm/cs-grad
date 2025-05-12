import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

def classify_points_svm(X, y):
    """
    Classify points using a linear SVM and return accuracy, precision, recall, F1 score, and line coefficients.

    Parameters:
    - X (np.array): A dataset with x, y coordinates. Shape should be (n_samples, 2).
    - y (np.array): Labels corresponding to each data point in X.
    - plot_boundary (bool): If True, plot the decision boundary.

    Returns:
    - tuple: accuracy, precision, recall, F1 score, line coefficients (a, b, c)
    """
    
    # Train a linear SVM
    clf = SVC(kernel='linear')
    clf.fit(X, y)

    return clf

def metrics_svm(X, y, clf, plot_boundary=False):
    # Predict the labels for the test set
    y_pred = clf.predict(X)

    # Calculate metrics
    accuracy = accuracy_score(y, y_pred)
    precision = precision_score(y, y_pred, average='macro')
    recall = recall_score(y, y_pred, average='macro')
    f1 = f1_score(y, y_pred, average='macro')

    if plot_boundary:
        # Plot the decision boundary
        plt.scatter(X[:, 0], X[:, 1], c=y, cmap='rainbow')
        
        # Creating a mesh of points to plot in
        h = .02  # Step size in the mesh
        x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
        
        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        plt.contourf(xx, yy, Z, cmap='rainbow', alpha=0.8)
        plt.title('Decision Boundary')
        plt.xlabel('X-coordinate')
        plt.ylabel('Y-coordinate')
        plt.show()

    a, b = clf.coef_[0]

    return accuracy, precision, recall, f1, (a, b)