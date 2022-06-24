from config import Config
from helpers import Helpers
from matrices import Matrices


class DES:
    def __init__(self):
        self.password = None
        self.text = None
        self.keys = list()

    def run(self, key, text, action=Config.ENCRYPT, padding=False):
        self.password = key
        self.text = text

        self.check_key()
        self.check_text(padding, action)

        self.generate_keys()

        # Split the text in blocks of 64 bits
        text_blocks = Helpers.n_split(self.text, 8)
        result = list()
        for block in text_blocks:
            block = self.get_permutated_block(block)

            left, right = Helpers.n_split(block, 32)
            tmp = None
            for i in range(16):
                # Expand d to match Ki size
                d_e = self.expand(right, Matrices.expansion_table)
                # If encrypt use Ki
                if action == Config.ENCRYPT:
                    tmp = self.xor(self.keys[i], d_e)
                # If decrypt start by the last key
                else:
                    tmp = self.xor(self.keys[15 - i], d_e)

                tmp = self.substitute(tmp)
                tmp = self.permutation(tmp, Matrices.permutation_function)
                tmp = self.xor(left, tmp)
                left = right
                right = tmp
            # Do the last permutation and add to result
            result += self.permutation(right + left, Matrices.inverse_initial_permutation)
        final_res = Helpers.bit_array_to_string(result)
        if padding and action == Config.DECRYPT:
            return self.remove_padding(final_res)  # Remove the padding if decrypt and padding is true
        else:
            return final_res  # Return the final string of data ciphered/deciphered

    def substitute(self, d_e):
        """
          # Substitute bytes using substitution boxes
        Args:
            d_e (list):

        Returns:

        """
        sub_blocks = Helpers.n_split(d_e, 6)  # Split bit array into sublist of 6 bits
        result = list()
        for i, block in enumerate(sub_blocks):
            block = sub_blocks[i]
            row = int(str(block[0]) + str(block[5]), 2)  # Get the row with the first and last bit
            column = int(''.join([str(x) for x in block[1:][:-1]]), 2)
            val = Matrices.substitution_boxes[i][row][column]  # Take the value in the SBOX appropriated for the round (i)
            bin = Helpers.bin_value(val, 4)  # Convert the value to binary
            result += [int(x) for x in bin]  # And append it to the resulting list
        return result

    def permutation(self, block, table):
        """
        Calculates permutation of given block with using given table
        Args:
            block (list): bit array of text block
            table (list): permutation table

        Returns:
            list
        """
        return [block[x - 1] for x in table]

    def expand(self, block, table):
        """
        Expands given block with given table
        Args:
            block (list): bit array of text block
            table (list): permutation table

        Returns:
            list
        """
        return [block[x - 1] for x in table]

    def xor(self, t1, t2):
        """
        Applies an xor to given list og bits and returns result
        Args:
            t1 (list): key value
            t2 (list): expanded and permutated value of text block

        Returns:
            list
        """
        return [x ^ y for x, y in zip(t1, t2)]

    def generate_keys(self):
        """
        Generates all the 16 keys
        Returns:
            None
        """
        self.keys = []
        key = Helpers.string_to_bit_array(self.password)
        key = self.permutation(key, Matrices.permuted_choice_1)
        # Split keys in to left and right pairs
        left, right = Helpers.n_split(key, 28)
        # Generate 16 keys
        for i in range(16):
            left, right = self.shift(left, right, Matrices.SHIFT[i])
            tmp = left + right  # Merge them
            self.keys.append(self.permutation(tmp, Matrices.permuted_choice_2))

    def shift(self, left, right, n):
        """
        Shifts key values according to given shift value
        Args:
            left (list): left side of key
            right (list): right side of key
            n (int): shift value

        Returns:
            list
        """
        return left[n:] + left[:n], right[n:] + right[:n]

    def add_padding(self):
        """
        Adds space to be a multiple of 8 if the text length is different than a multiple of 8.
        Returns:
            None
        """
        pad_len = 8 - (len(self.text) % 8)
        self.text += pad_len * " "

    def remove_padding(self, data):
        """
        Removes padding to the text
        Args:
            data (list): text

        Returns:
            list
        """
        pad_len = ord(data[-1])
        return data[:-pad_len]

    def check_key(self):
        if len(self.password) < 8:
            raise Exception("Key Should be 8 bytes long")
        # If key size is above 8bytes, cut to be 8bytes long
        if len(self.password) > 8:
            self.password = self.password[:8]

    def check_text(self, padding, action):
        if padding and action == Config.ENCRYPT:
            self.add_padding()
        elif len(self.text) % 8 != 0:
            raise Exception("Data size should be multiple of 8")

    def get_permutated_block(self, block):
        # Convert the block in bit array
        block = Helpers.string_to_bit_array(block)
        # Apply the initial permutation
        block = self.permutation(block, Matrices.initial_permutation)

        return block

    def encrypt(self, key, text, padding=False):
        return self.run(key, text, Config.ENCRYPT, padding)

    def decrypt(self, key, text, padding=False):
        return self.run(key, text, Config.DECRYPT, padding)
