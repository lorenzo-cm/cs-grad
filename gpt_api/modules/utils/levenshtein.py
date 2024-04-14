import numpy as np

keyboard_layout = {
    'q': (0, 0), 'w': (0, 1), 'e': (0, 2), 'r': (0, 3), 't': (0, 4), 'y': (0, 5), 'u': (0, 6), 'i': (0, 7), 'o': (0, 8), 'p': (0, 9),
    'a': (1, 0), 's': (1, 1), 'd': (1, 2), 'f': (1, 3), 'g': (1, 4), 'h': (1, 5), 'j': (1, 6), 'k': (1, 7), 'l': (1, 8), 'ç': (1, 9),
    'z': (2, 0), 'x': (2, 1), 'c': (2, 2), 'v': (2, 3), 'b': (2, 4), 'n': (2, 5), 'm': (2, 6)
}

def key_distance(char1, char2):
    if char1 in keyboard_layout and char2 in keyboard_layout:
        coord1 = np.array(keyboard_layout[char1])
        coord2 = np.array(keyboard_layout[char2])
        distance = np.linalg.norm(coord1 - coord2)
        # Scale down the distance so that adjacent keys have a distance close to 1
        return 0.5 * distance + 0.5
    return 1  # default distance if key not found

def modified_levenshtein(s1, s2):
    s1 = s1.lower()
    s2 = s2.lower()
    m, n = len(s1), len(s2)
    dp = np.zeros((m+1, n+1))

    for i in range(m+1):
        for j in range(n+1):
            if i == 0:
                dp[i, j] = j
            elif j == 0:
                dp[i, j] = i
            elif s1[i-1] == s2[j-1]:
                dp[i, j] = dp[i-1, j-1]
            else:
                dp[i, j] = min(
                    dp[i-1, j] + 1,
                    dp[i, j-1] + 1,
                    dp[i-1, j-1] + key_distance(s1[i-1], s2[j-1])
                )
    return dp[m, n]

def normalized_distance(s1, s2):
    raw_distance = modified_levenshtein(s1, s2)
    penalty = raw_distance ** 2.5
    normalization_factor = ((len(s1) + len(s2)) / 2) ** 1.5
    return penalty / normalization_factor

def get_closest_match(s, candidates:list[str]) -> tuple[str, float]:
    best_match = None
    best_distance = float('inf')
    for candidate in candidates:
        distance = normalized_distance(s, candidate)
        if distance < best_distance:
            best_match = candidate
            best_distance = distance
    return (best_match, best_distance) if best_distance < 0.75 else ('', best_distance)