import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

def apply_pca(data, labels, target_names=None, visualize=False):
    """
    Apply PCA to reduce the dataset to 2 components.
    
    Parameters:
    - data: The dataset to be reduced.
    - labels: The labels or classes of the dataset.
    - target_names: Names of the classes for visualization.
    - visualize: Boolean indicating if the data should be visualized.
    
    Returns:
    - 2D reduced dataset.
    """

    # Apply PCA and reduce the dataset to 2 components
    pca = PCA(n_components=2)
    data_pca = pca.fit_transform(data)

    # Visualization
    if visualize:
        plt.figure(figsize=(10, 6))
        
        # If target names are not provided, use unique labels
        if target_names is None:
            target_names = np.unique(labels)
        
        colors = plt.cm.rainbow(np.linspace(0, 1, len(target_names)))
        
        for color, target in zip(colors, target_names):
            plt.scatter(data_pca[labels == target, 0], data_pca[labels == target, 1], color=color, label=target, edgecolor='k')

        
        plt.legend()
        plt.xlabel('Principal Component 1')
        plt.ylabel('Principal Component 2')
        plt.title('2D PCA of Dataset')
        plt.show()

    return data_pca