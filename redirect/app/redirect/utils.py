from string import ascii_letters
from random import randint

LENGTH = len(ascii_letters)

def generate_path():

    path = ''

    for _ in range(0, 10):

        path += ascii_letters[randint(0, LENGTH)]

    return path
    