from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib

from .hog_op import compute_hog_X

def train_hog(X_train, y_train, orientations=9, pixels_per_cell=(8,8), cells_per_block=(2,2)):
    X_train_hog = compute_hog_X(X_train,
                                orientations,
                                pixels_per_cell,
                                cells_per_block)
    classifier = SVC(kernel='linear', probability=True)
    
    classifier.fit(X_train_hog, y_train)
    return classifier
    
def test_hog(classifier, X_test, y_test, orientations=9, pixels_per_cell=(8,8), cells_per_block=(2,2)):
    X_test_hog = compute_hog_X(X_test,
                               orientations,
                               pixels_per_cell,
                               cells_per_block)

    y_pred = classifier.predict(X_test_hog)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy * 100:.2f}%")
    return accuracy

def save_hog(classifier, path):
    joblib.dump(classifier, path)
    return True
    
def load_hog(path):
    return joblib.load(path)