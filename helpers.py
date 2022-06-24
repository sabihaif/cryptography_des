
class Helpers:
    @staticmethod
    def string_to_bit_array(text):  # Convert a string into a list of bits
        array = list()
        for char in text:
            binval = Helpers.bin_value(char, 8)  # Get the char value on one byte
            array.extend([int(x) for x in list(binval)])  # Add the bits to the final list
        return array

    @staticmethod
    def bit_array_to_string(array):  # Recreate the string from the bit array
        res = ''.join([chr(int(y, 2)) for y in [''.join([str(x) for x in _bytes]) for _bytes in Helpers.n_split(array, 8)]])
        return res

    @staticmethod
    def bin_value(val, bitsize):  # Return the binary value as a string of the given size
        binval = bin(val)[2:] if isinstance(val, int) else bin(ord(val))[2:]
        if len(binval) > bitsize:
            raise Exception("binary value larger than the expected size")
        while len(binval) < bitsize:
            binval = "0" + binval  # Add as many 0 as needed to get the wanted size
        return binval

    @staticmethod
    def n_split(s, n):  # Split a list into sub lists of size "n"
        return [s[k:k + n] for k in range(0, len(s), n)]

    @staticmethod
    def add_padding(text):
        pad_len = 8 - (len(text) % 8)
        text += pad_len * " "
