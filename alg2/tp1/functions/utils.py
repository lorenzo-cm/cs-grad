import matplotlib.pyplot as plt
import seaborn as sns
import time
import numpy as np

anchor:int

class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f'Point({self.x},{self.y})'
    
    def __eq__(self, p1) -> bool:
        return True if (self.x == p1.x and self.y == p1.y) else False
    
    def __iter__(self):
        return iter((self.x, self.y))
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Point indices must be 0 or 1")
        
    def round(self, decimals=5):
        return Point(round(self.x, decimals), round(self.y, decimals))


class Segment:
    def __init__(self, p1: Point, p2: Point):
        self.points = [p1, p2]

    def __repr__(self) -> str:
        return f'Segment({self.points[0]}, {self.points[1]})'

    def __eq__(self, other):
        return self.points == other.points
    
    def __hash__(self) -> int:
        return hash(tuple(self.points))
    
    def round(self, decimals=5):
        return Segment(self.points[0].round(decimals), self.points[1].round(decimals))
    

def orientation(p0: Point, p1: Point, p2: Point) -> int:
    val = (p1.x - p0.x) * (p2.y - p1.y) - (p1.y - p0.y) * (p2.x - p1.x)
    if val == 0: return 0  # colinear
    return 1 if val > 0 else -1  # counterclockwise or clockwise


def compare_points(p1: Point, p2: Point) -> int:
    o = orientation(anchor, p1, p2)
    if o == 0:
        # If colinear, sort by distance to anchor
        d1 = (p1.x - anchor.x)**2 + (p1.y - anchor.y)**2
        d2 = (p2.x - anchor.x)**2 + (p2.y - anchor.y)**2
        return -1 if d1 < d2 else 1
    return o


def points_to_segments(points: list[Point]) -> list[Segment]:
    segments = []
    for i in range(len(points)):
        segments.append(Segment(points[i], points[(i+1) % len(points)]))
    return segments


def plot_grid_hulls_separation(X, y, 
                               hull1: list[Point], hull2: list[Point], 
                               ab: tuple, ab_svm: tuple, ab_p: tuple,
                               save=False, plot=True, filename=""):
    
    margin_x = 0.5
    margin_y = 0.5

    plt.figure(figsize=(10, 8))
    sns.set_style("whitegrid")
    
    # Plotting the points using seaborn
    sns.scatterplot(x=X[:, 0], y=X[:, 1], hue=y, palette="rainbow", edgecolor="k", s=100)
    
    # Plotting the convex hulls
    hull1_points = [(point.x, point.y) for point in hull1]
    hull2_points = [(point.x, point.y) for point in hull2]
    hull1_points.append(hull1_points[0])  # To close the hull
    hull2_points.append(hull2_points[0])  # To close the hull

    plt.plot([point[0] for point in hull1_points], [point[1] for point in hull1_points], 'r-')
    plt.plot([point[0] for point in hull2_points], [point[1] for point in hull2_points], 'r-')
    
    # Determine plot limits based on convex hulls
    min_x = min(hull1_points + hull2_points, key=lambda t: t[0])[0] - margin_x
    max_x = max(hull1_points + hull2_points, key=lambda t: t[0])[0] + margin_x
    min_y = min(hull1_points + hull2_points, key=lambda t: t[1])[1] - margin_y
    max_y = max(hull1_points + hull2_points, key=lambda t: t[1])[1] + margin_y
    
    plt.xlim(min_x, max_x)
    plt.ylim(min_y, max_y)
    
    # Plotting the lines
    x_values = np.linspace(min_x, max_x, 400)
    
    # y = ax + b (for our model, color blue)
    y_values = [ab[0]*x + ab[1] for x in x_values]
    plt.plot(x_values, y_values, 'b-', label='Our Model')
    
    # y = ax + b (for svm model, color green)
    y_values_svm = [ab_svm[0]*x + ab_svm[1] for x in x_values]
    plt.plot(x_values, y_values_svm, 'g-', label='SVM Model')
    
    # y = ax + b (perpendicular line, color gray)
    y_values_perpendicular = [ab_p[0]*x + ab_p[1] for x in x_values]
    plt.plot(x_values, y_values_perpendicular, 'k-', label='Perpendicular Line')
    
    plt.legend()

    # If save option is enabled

    if plot:
        plt.show()
        
    if save:
        plt.savefig(filename)
        

def timer(func):
    def wrapper(*args, **kwargs):
        use_timer = kwargs.pop('use_timer', True)
        if use_timer:
            start_time = time.perf_counter()  # Begin the timer
            result = func(*args, **kwargs)    # Call the actual function
            end_time = time.perf_counter()    # End the timer
            elapsed_time = end_time - start_time
            return result, elapsed_time
        else:
            return func(*args, **kwargs)  # Call the function without timing
    return wrapper