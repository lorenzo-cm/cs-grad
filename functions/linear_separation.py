from functions.utils import Point, timer
import numpy as np

# does not need to be super fast because it is used in hulls
def find_closest_points(hull1, hull2) -> tuple[Point, Point]:
    min_distance = float('inf')
    closest_pair = (None, None)

    for p1 in hull1:
        for p2 in hull2:
            distance = np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
            if distance < min_distance:
                min_distance = distance
                closest_pair = (p1, p2)

    return closest_pair

def find_line_coefficients(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    # Vertical line
    if x1 == x2:
        return (float('inf'), x1)

    # Horizontal line
    if y1 == y2:
        return (0, y1)

    # Slope (a) for other cases
    a = (y2 - y1) / (x2 - x1)
    
    # y-intercept (b)
    b = y1 - a * x1

    return a, b

@timer
def linear_separation(hull1, hull2):
    p1, p2 = find_closest_points(hull1, hull2)

    a_p1, b_p1 = find_line_coefficients(p1, p2)

    a = -1 / a_p1

    b = p1.y - a * p1.x

    return a, b, a_p1, b_p1
