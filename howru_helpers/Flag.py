OFFSET = 127462 - ord('A')


def flag(code):
    code = code.upper()
    return chr(ord(code[0]) + OFFSET) + chr(ord(code[1]) + OFFSET)


def unflag(msg):
    return chr(ord(msg[0]) - OFFSET) + chr(ord(msg[1]) - OFFSET)