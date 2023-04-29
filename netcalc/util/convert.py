class BinaryConvertException(Exception):
    def __init__(self, message=None):
        self.message = "Error when trying to convert to binary"

        if message:
            super().__init__(message)
        else:
            super().__init__(self.message)

def bd(binary: str) -> str:
    if binary.count('0') + binary.count('1') != len(binary):
        return ValueError("The value {} is not binary".format(binary))
    
    decimal = 0
    for i, c in enumerate(binary[::-1]):
        decimal += int(c) * (2 ** i)

    return decimal

def db(decimal: int | str, bit_repr: int = 0) -> str:
    decimal_str = bin(int(decimal)).replace('0b', '')

    if int(decimal) == 0:
        if bit_repr:
            return '0' * bit_repr

        return '0'

    if bit_repr == 0:
        return decimal_str

    if bit_repr > len(decimal_str):
        decimal_str = ('0' * (bit_repr - len(decimal_str))) + decimal_str
        return decimal_str
    
    if bit_repr < len(decimal_str):
        raise BinaryConvertException("The representation of decimal '{}' in bits does not support {} bits".format(decimal, bit_repr))

    else:
        return decimal_str

def bh(binary: str) -> str:
    decimal = bd(binary)

    return hex(decimal).replace('0x', '')

def hb(hex_: str, bit_repr: int = 0) -> str:
    if hex_.startswith('0x'):
        hex_ = hex_[2:]

    hexadecimal_chars = "0123456789ABCDEF"
    hexadecimal_letters = {'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}

    binary = ""
    for h in hex_.upper():
        if not h in hexadecimal_chars:
            raise ValueError("The value '{}' is not a valid hexadecimal!".format(hex_))

        try:
            binary += db(int(h), 4)
        except ValueError:
            binary += db(hexadecimal_letters[h])

    if bit_repr == 0:
        return binary

    if bit_repr < len(binary):
         raise BinaryConvertException("The representation of hex '{}' in bits does not support {} bits".format(decimal, bit_repr))

    return ('0' * (bit_repr - len(binary))) + binary

def hd(hex_: str) -> str:
    return bd(hb(hex_))

def dh(decimal: str | int) -> str:
    return bh(db(decimal))
