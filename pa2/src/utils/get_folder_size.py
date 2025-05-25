import os

def get_folder_size(folder) -> int:
    total_size = 0

    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)

            if os.path.isfile(filepath):
                total_size += os.path.getsize(filepath)

    return total_size
