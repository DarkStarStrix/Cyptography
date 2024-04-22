# code RSA algorithm in python between two parties

import random
import math
import argparse
import os
import json


class RSA:
    def __init__(self):
        self.prime = 0
        self.prime1 = 0
        self.n = 0
        self.phi = 0
        self.e = 0
        self.d = 0

    @staticmethod
    def is_prime(num):
        if num == 2:
            return True
        if num < 2 or num % 2 == 0:
            return False
        for i in range (3, int (math.sqrt (num)) + 1, 2):
            if num % i == 0:
                return False
        return True

    def generate_prime(self):
        while True:
            self.prime = random.randint (100, 1000)
            if self.is_prime (self.prime):
                break
        while True:
            self.prime1 = random.randint (100, 1000)
            if self.is_prime (self.prime1):
                break

    def generate_keys(self):
        self.n = self.prime * self.prime1
        self.phi = (self.prime - 1) * (self.prime1 - 1)
        while True:
            self.e = random.randint (2, self.phi - 1)
            if math.gcd (self.e, self.phi) == 1:
                break
        for i in range (1, self.phi):
            if (self.e * i) % self.phi == 1:
                self.d = i
                break

    def encrypt(self, message):
        return [pow (ord (char), self.e, self.n) for char in message]

    def decrypt(self, cipher):
        return ''.join ([chr (pow (char, self.d, self.n)) for char in cipher])

    def save_keys(self, filename):
        with open (filename, 'w') as f:
            json.dump ({'e': self.e, 'd': self.d, 'n': self.n}, f)

    def load_keys(self, filename):
        with open (filename, 'r') as f:
            keys = json.load (f)
            self.e = keys ['e']
            self.d = keys ['d']
            self.n = keys ['n']


def main():
    parser = argparse.ArgumentParser (description='RSA encryption and decryption.')
    parser.add_argument ('message', type=str, help='The message to encrypt or decrypt.')
    parser.add_argument ('--decrypt', action='store_true', help='Decrypt the message.')
    parser.add_argument ('--keyfile', type=str, default='keys.json', help='The file to save/load the keys.')
    args = parser.parse_args ()

    rsa = RSA ()
    if os.path.exists (args.keyfile):
        rsa.load_keys (args.keyfile)
    else:
        rsa.generate_prime ()
        rsa.generate_keys ()
        rsa.save_keys (args.keyfile)

    if args.decrypt:
        cipher = [int (x) for x in args.message.split (',')]
        print ("Decrypted message: ", rsa.decrypt (cipher))
    else:
        cipher = rsa.encrypt (args.message)
        print ("Encrypted message: ", ','.join (map (str, cipher)))


if __name__ == "__main__":
    main ()
