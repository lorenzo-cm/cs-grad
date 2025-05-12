import numpy as np
import pandas as pd
from sklearn.datasets import load_iris, load_wine, load_digits, load_breast_cancer


from utils import *
from graham_scan import graham_scan
from sweep_line_intersection import sweep_line_intersection
from datasets import *
from linear_separation import linear_separation
from linear_classification import linear_classification
from svm import classify_points_svm, metrics_svm
from pca import apply_pca


if __name__ == '__main__':

    np.random.seed(42)

    time_load_dataset = time_hull = time_intersection = time_linear_sep = time_linear_class = 0

    for d_name, d in datasets.items():

        print(f"Dataset: {d_name}")

        # load the dataset

        init = time.perf_counter()
        df = d()
        time_load_dataset += time.perf_counter() - init

        # verify if it is a binary classification problem
        unique_classes = np.unique(df['target'])
        if unique_classes.size > 2:
            # randomly select 2 classes
            selected_classes = np.random.choice(unique_classes, 2, replace=False)

            filtered_df = df[df['target'].isin(selected_classes)]

        if df.shape[1] > 3: # 3 because of target
            # Extract data and labels from the filtered dataframe
            X_filtered = filtered_df.drop('target', axis=1).values
            y_filtered = filtered_df['target'].values

            # Apply PCA and visualize the result
            reduced_data = apply_pca(X_filtered, y_filtered, target_names=selected_classes)

        reduced_df = pd.DataFrame(reduced_data, columns=['x', 'y'])
        reduced_df['target'] = y_filtered

        # select 70% of the data for training and 30% for testing
        train_df = reduced_df.sample(frac=0.7)

        # grab 30% of the data for testing
        test_df = reduced_df.drop(train_df.index)

        # reset the index
        train_df = train_df.reset_index(drop=True)
        test_df = test_df.reset_index(drop=True)

        # TRAINING PHASE

        X1 = train_df[train_df['target'] == selected_classes[0]][['x', 'y']]
        X2 = train_df[train_df['target'] == selected_classes[1]][['x', 'y']]

        # making the hull for each
        hull1, time1_ = graham_scan([Point(row['x'], row['y']) for _, row in X1.iterrows()])
        hull2, time2_ = graham_scan([Point(row['x'], row['y']) for _, row in X2.iterrows()])

        time_hull += time1_
        time_hull += time2_

        all_segments1 = points_to_segments([Point(row['x'], row['y']) for _, row in X1.iterrows()])
        all_segments2 = points_to_segments([Point(row['x'], row['y']) for _, row in X2.iterrows()])

        # round segments

        all_segments1 = [s.round() for s in all_segments1]
        all_segments2 = [s.round() for s in all_segments2]
            

        intersection = True

        (intersection, collided_segments), time_ = sweep_line_intersection(all_segments1, all_segments2)

        time_intersection += time_

        if intersection:
            print("Intersects\n")
            print("Removing intersect points...")

            counter = 0
            while intersection:
                (intersection, collided_segments), time_ = sweep_line_intersection(all_segments1, all_segments2)

                time_intersection += time_
                for segment1, segment2 in collided_segments:
                    for s in all_segments1:
                        if s == segment1 or s == segment2:
                            all_segments1.remove(s)
                            
                    for s in all_segments2:
                        if s == segment1 or s == segment2:
                            all_segments2.remove(s)

                counter += 1

            print(f'Number of iterations removing intersect points: {counter}')

        print("Not intersects")

        # ax + by + c = 0
        (a, b, a_p1, a_p2), time_ = linear_separation(hull1, hull2)

        time_linear_sep += time_

        clf = classify_points_svm(train_df[['x', 'y']].values, train_df['target'].values)

        # TESTING PHASE
        
        # X = train_df[['x', 'y']].values
        # y = train_df['target'].values

        X = test_df[['x', 'y']].values
        y = test_df['target'].values

        acc_svm, precision_svm, recall_svm, f1_svm, ab_svm = metrics_svm(X, y, clf)

        (acc, precision, recall, f1), time_ = linear_classification(X, y, a, b, selected_classes[0], selected_classes[1])


        time_linear_class += time_

        print(f"METRICS: Accuracy: {acc}, Precision: {precision}, Recall: {recall}, F1 Score: {f1}")

        print(f"METRICS SVM: Accuracy: {acc_svm}, Precision: {precision_svm}, Recall: {recall_svm}, F1 Score: {f1_svm}")

        # Plotting the data
        plot_grid_hulls_separation(X, y, hull1, hull2, (a, b), ab_svm, (a_p1, a_p2), save=True, filename=f"graphs/dataset_{d_name}.png")

        print()
    
    print(f"Time load dataset: {time_load_dataset}")
    print(f"Time hull: {time_hull}")
    print(f"Time intersection: {time_intersection}")
    print(f"Time linear separation: {time_linear_sep}")
    print(f"Time linear classification: {time_linear_class}")
