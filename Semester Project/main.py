#!/usr/bin/env python3

import os.path
import sys
from Crypto import Random
from Crypto.Cipher import  PKCS1_OAEP
from Crypto.PublicKey import RSA
import os
from cryptography.fernet import Fernet
from query import patient_query, auditor_query
from immutability import check_integrity, hashFunction
from user_authentication import register_user, authenticate_auditor, authenticate_patient


class Fernet_Encrypt:
    def __init__(self) -> None:
        self.key = Fernet.generate_key()
        self.keyPair = RSA.generate(2048)
        f = open("audit_log_keypair.pem", 'wb')
        f.write(self.keyPair.export_key('PEM'))
        f.close()
    
    def encrypt(self, file):
        with open(file, 'rb') as f:
            raw = f.read()
        fernet = Fernet(self.key)
        encrypted = fernet.encrypt(raw)

        with open("audit_log.csv.enc", 'wb') as f:
            f.write(encrypted)
        
        pubkey = self.keyPair.publickey()
        encrpytor = PKCS1_OAEP.new(pubkey)
        encrypted_key = encrpytor.encrypt(self.key)

        with open('adl.csv.key', 'wb') as f:
            f.write(encrypted_key)


def choice(option):
    if option == 1:
        register_user()
    elif option == 2:
        user = str(input("Pleae enter the user ('patient' or 'auditor') you are attempting to query as: "))
        RSAfile = str(input("Please provide your RSA key file: "))
        id = int(input("Please enter your "+user+' ID: '))
        if user == 'patient':
            flag, user_id = authenticate_patient(RSAfile, id)
            if flag == False:
                return
            patient_query(id)
        else:
            flag, user_id = authenticate_auditor(RSAfile, id)
            if flag == False:
                return
            auditor_query(id)
    elif option == 3:
        user = str(input("Pleae enter the user ('patient' or 'auditor') you are attempting to query as: "))
        RSAfile = str(input("Please provide your RSA key file: "))
        id = int(input("Please enter your "+user+' ID: '))
        if user == 'patient':
            flag, user_id = authenticate_patient(RSAfile, id)
            if flag == False:
                return
            check_integrity(id, user_id)
        else:
            flag, user_id = authenticate_auditor(RSAfile, id)
            if flag == False:
                return
            check_integrity(id, user_id)

    else:
        ('Please select a correct option.')


if __name__ == "__main__":
    
    if os.path.exists('audit_log.csv'):
        f = open('og_audit_log.txt', 'w')
        f.write(hashFunction('audit_log.csv'))
        f.close()
        encryption = Fernet_Encrypt()
        encryption.encrypt('audit_log.csv')        
        os.remove('audit_log.csv')
    
    while True:
        print('                                                                                                                         ')
        print('****************************************************************************************************************')
        print("Welcome to the Secure Decentralized Audit System")
        print("Please enter an option out of the following:")
        print("1. Register a User")
        print("2. Query audit records")
        print("3. Immutability verification")
        print("4. Exit System")       
        option = int(input("Choice: "))
        if option == 4:
            print("Thank you for using the system!")
            break
        choice(option)