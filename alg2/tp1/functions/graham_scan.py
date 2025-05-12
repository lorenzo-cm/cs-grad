import numpy as np
from functools import cmp_to_key

from functions.utils import *
import functions.utils as utils


@timer
def graham_scan(points: list[Point]) -> list[Point]:

    if len(points) < 3:
        return points

    # Anchor point with the lowest y-coordinate
    anchor = min(points, key=lambda p: (p.y, p.x))
    utils.anchor = anchor

    # bigger angle go first
    sorted_points = sorted(points, key=cmp_to_key(compare_points))

    stack = list()
    stack.append(sorted_points[0])
    stack.append(sorted_points[1])
    stack.append(sorted_points[2])

    # left to right orientation of hull
    for i in range(3, len(sorted_points)):
        while len(stack) > 1 and orientation(stack[-2], stack[-1], sorted_points[i]) >= 0:
            stack.pop()
        stack.append(sorted_points[i])

    return stack
