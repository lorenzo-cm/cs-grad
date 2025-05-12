all_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ?"

char_to_int = {char: idx for idx, char in enumerate(all_chars)}

int_to_char = {idx: char for idx, char in enumerate(all_chars)}

def convert_char_to_int(char: str):
    return char_to_int[char.upper()]

def convert_int_to_char(num: int):
    return int_to_char[num]

if __name__ == '__main__':
    print(convert_char_to_int('?'))
    print(convert_int_to_char(35))
