import random
CHARS = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя.,\''


def encrypt(msg, key):
    key_list = list(key)
    matrix = [key_list[i * 6:(i + 1) * 6] for i in range(6)]
    char_to_index = {}
    index_to_char = []
    for row, column_values in enumerate(matrix):
        index_to_char.append([])
        for column, char in enumerate(column_values):
            char_to_index[char] = [row, column]
            index_to_char[row].append(char)
    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                     for row in index_to_char]))
    indexes = [[], []]
    for char in list(msg):
        coord = char_to_index[char]
        indexes[0].append(coord[0])
        indexes[1].append(coord[1])
    joined = indexes[0] + indexes[1]
    result = ''
    for i in range(0, len(joined), 2):
        result += index_to_char[joined[i]][joined[i+1]]
    return result


def decrypt(msg, key):
    key_list = list(key)
    matrix = [key_list[i * 6:(i + 1) * 6] for i in range(6)]
    char_to_index = {}
    index_to_char = []
    for row, column_values in enumerate(matrix):
        index_to_char.append([])
        for column, char in enumerate(column_values):
            char_to_index[char] = [row, column]
            index_to_char[row].append(char)
    joined = []
    for char in list(msg):
        coord = char_to_index[char]
        joined.append(coord[0])
        joined.append(coord[1])
    indexes = [joined[:len(joined) // 2], joined[len(joined) // 2:]]
    result = ''
    for i in range(len(indexes[0])):
        result += index_to_char[indexes[0][i]][indexes[1][i]]
    return result


userMessage = input('Enter message to be encrypted:')

encrypted = encrypt(userMessage, CHARS)
print('Your encrypted with key[{0}] message:'.format(CHARS))
print(encrypted)

decrypted = decrypt(encrypted, CHARS)
print('Your decrypted message:')
print(decrypted)

shuffled_key = ''.join(random.sample(CHARS,len(CHARS)))
encrypted = encrypt(userMessage, shuffled_key)
print('Your encrypted with key[{0}] message:'.format(shuffled_key))
print(encrypted)

decrypted = decrypt(encrypted, shuffled_key)
print('Your decrypted message:')
print(decrypted)
