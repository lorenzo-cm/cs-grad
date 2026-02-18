import numpy as np
import time

def euclidean_distance(coord1, coord2):
    """Calcula a distância euclidiana entre dois pontos."""
    return np.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # Start timing
        result = func(*args, **kwargs)    # Call the function
        end_time = time.perf_counter()    # End timing
        time_taken = end_time - start_time  # Calculate elapsed time
        minutes = time_taken // 60
        seconds = time_taken % 60
        print(f"{minutes:.0f} minutes and {seconds:.3f} seconds to execute")
        return result
    return wrapper
