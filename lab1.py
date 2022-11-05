def encrypt(msg, column, row):
    column_length = len(column)
    row_length = len(row)
    if column_length * row_length < len(msg):
        raise Exception("Invalid keys")
    msg = msg.ljust(column_length * row_length)
    msg_list = list(msg)

    # using list comprehension
    matrix = [msg_list[i * column_length:(i + 1) * column_length] for i in range((len(msg_list) + column_length - 1)
                                                                                 // column_length)]

    column_order = dict(sorted({k: v for v, k in enumerate(list(column))}.items())).values()
    row_order = dict(sorted({k: v for v, k in enumerate(list(row))}.items())).values()

    result = ''
    for i in row_order:
        result += (''.join([matrix[i][j] for j in column_order]))
    return result


def decrypt(msg, column, row):
    column_length = len(column)
    row_length = len(row)
    if column_length * row_length < len(msg):
        raise Exception("Invalid keys")
    msg = msg.ljust(column_length * row_length)
    msg_list = list(msg)

    # using list comprehension
    matrix = [msg_list[i * column_length:(i + 1) * column_length] for i in range((len(msg_list) + column_length - 1)
                                                                                 // column_length)]

    column_order = dict(sorted({letter: index for index, letter in enumerate(list(column))}.items())).values()
    column_order = dict(sorted({index: inverted for inverted, index in enumerate(column_order)}.items())).values()
    row_order = dict(sorted({letter: index for index, letter in enumerate(list(row))}.items())).values()
    row_order = dict(sorted({index: inverted for inverted, index in enumerate(row_order)}.items())).values()

    result = ''
    for i in row_order:
        result += (''.join([matrix[i][j] for j in column_order]))
    return result


columnKey = input('Enter column key:')
rowKey = input('Enter row key:')
userMessage = input('Enter message to be encrypted:')
encrypted = encrypt(userMessage, columnKey, rowKey)

decrypted = decrypt(encrypted, columnKey, rowKey)
print('Your encrypted message:')
print(encrypted)

print('Your decrypted message:')
print(decrypted)
