#!/usr/bin/env python3

from cgitb import text
import sys, base64
from Crypto import Random
from Crypto.Cipher import AES
import hashlib, os

ENCODE_FORMAT = 'utf-8'


class AESCipher:
    def __init__(self, key) -> None:
        self.key = key
        self.bs = 16

    # def pad(self,message):
    #     nofbytes = self.bs - len(message) % self.bs
    #     extraString = nofbytes * chr(nofbytes)
    #     return message + extraString

    # @staticmethod
    # def unpad(message):
    #     return message[:-ord(message[len(message)-1:])]

    def encrypt(self, file):
        with open(file, 'r') as f:
            plaintext = f.read()

        pad = lambda s: s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
        raw = base64.b64encode(pad(plaintext).encode('utf8'))

        iv = Random.new().read(self.bs)

        encoded_key = hashlib.sha256(str(self.key).encode(ENCODE_FORMAT)).digest()

        cipher = AES.new(encoded_key, AES.MODE_CBC,iv)
        encrypted = cipher.encrypt(raw)

        encoded = base64.b64encode(iv+encrypted)
        return str(encoded, ENCODE_FORMAT)

    @staticmethod
    def decrypt(cip_file, text_file, key_file):

        block_size = 16
        unpad = lambda s: s[:-ord(s[-1:])]

        n, d = key_file_extraction(key_file)

        with open(cip_file, 'r') as f:
            encrypted_text = f.read()

        ciphertext, enc_key = encrypted_text.split(',')
        enc_key = int(enc_key)
        key = pow(enc_key, d, n)

        key = hashlib.sha256(str(key).encode(ENCODE_FORMAT)).digest()
        decoded = base64.b64decode(ciphertext)
        iv = decoded[:block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(decoded[block_size:])
        clear_text = unpad(base64.b64decode(decrypted).decode(ENCODE_FORMAT))

        with open(text_file+".txt", 'w') as f:
            f.write(clear_text)


def key_file_extraction(key_file):
    with open(key_file, 'r') as f:
        data = f.read()

    N, E_D = data.split(',')

    return(int(N), int(E_D))

def encrypt_aes_key(rsa_key_file, aes_key):

    n, e = key_file_extraction(rsa_key_file)

    enc_key = pow(aes_key, e, n)
    return enc_key


if __name__ == "__main__":
    isDec = True
    if sys.argv[1] == '-e':
        isDec = False
    
    key = sys.argv[2]
    secret_file1 = sys.argv[3]
    secret_file2 = sys.argv[4]
    file_Name, format = secret_file2.split('.')
    if isDec == True:
        print("**************************************  Decryption Selected **************************************")
    else: print("**************************************  Encryption Selected **************************************")

    if not isDec:
        random_bytes = os.urandom(16)
        rand_key =  int.from_bytes(random_bytes, byteorder='little')
        encryption = AESCipher(rand_key)
        encrypted_key = encrypt_aes_key(key, rand_key)
        out = encryption.encrypt(secret_file1)
        with open(file_Name +".cip", 'w') as f:
            f.write(out + ',' + str(encrypted_key))

    else:
        AESCipher.decrypt(secret_file1, file_Name, key)
    