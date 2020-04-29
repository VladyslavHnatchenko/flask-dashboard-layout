import random
import os
import hashlib


class Encrypt:

    # Initializes the Class with the original text given
    def __init__(self, text):
        self.text = text

    # Get's the original text that has been hashed
    def get_hash(self, text):
        b = text.encode()
        hasher = hashlib.sha256()
        hasher.update(b)
        return str(hasher.hexdigest())

    # Gets the text and hashes it with the salt
    def get_hashed_salt(self):
        word = self.get_text()
        spot = random.randint(0, self.get_text_length() - 1)
        new_word = ''
        count = 0
        for c in word:
            new_word += c
            if count == spot:
                new_word += self.get_salt()
            count += 1
        hashed_word = self.get_hash(new_word)
        return hashed_word

    # Gets the hashed text with salt at a specific spot in the text
    def get_hashed_saltspot(self, spot):
        word = self.get_text()
        new_word = ''
        count = 0
        for c in word:
            new_word += c
            if count == spot:
                new_word += self.get_salt()
            count += 1

        hashed_word = self.get_hash(new_word)
        return hashed_word

    # Get's the ORIGINAL text that was given to the class
    def get_text(self):
        return self.text

    # Gets the ORIGINAL text length
    def get_text_length(self):
        return len(self.get_text())

    # Gets and returns the salt
    # In the future this will be read from a .json file or something
    def get_salt(self):
        return 'n3da942!#lnasf%7gpoo2bdjag'
