#!/usr/bin/env python3


import base64
import os.path
from Crypto import Random
from Crypto.Cipher import  PKCS1_OAEP
from Crypto.PublicKey import RSA
import os
from cryptography.fernet import Fernet
import json
from hashlib import sha256
import base64

def Fernetenc(key, raw):
    fernet = Fernet(key)
    result = fernet.encrypt(raw)
    return result

def Fernetdec(key, raw):
    fernet = Fernet(key)
    result = fernet.decrypt(raw)
    return result

def RSAenc(keyPair, input):
    pubkey = keyPair.publickey()
    encryptor = PKCS1_OAEP.new(pubkey)
    result = encryptor.encrypt(input)
    return result

def RSAdec(keyPair, input):
    decryptor = PKCS1_OAEP.new(keyPair)
    dec_key = decryptor.decrypt(input)
    return dec_key

def type_id(file):
    f = open(file)
    id_list = json.load(f)
    f.close()
    id = id_list.pop(0)
    f = open(file, 'w')
    json.dump(id_list,f)
    f.close()
    return id

def register_user():
    u_id = str(input("Please enter the name to be registered as User_ID: "))
    type = str(input("Please specify if you are a patient or an auditor: "))
    user_list={}
    if os.path.exists('authentication_server.json'):
        f = open('authentication_server.json', 'r')
        user_list = json.load(f)
        f.close()

    user_check = type+': '+u_id
    
    if user_check in user_list:
        print("The user is already present in the system. Please try a different user or select another option.")
        return
    
    if type == 'patient':
        id = type_id('p_id.json')
    else:
        id = type_id('a_id.json')

    key = Fernet.generate_key()
    keyPair = RSA.generate(2048)
    f = open(u_id+'.pem','wb')
    f.write(keyPair.export_key('PEM'))
    f.close()

    enc_uid = Fernetenc(key, u_id.encode('UTF-8'))
    enc_id = Fernetenc(key, str(id).encode('UTF-8'))
    DS = RSAenc(keyPair, enc_uid+enc_id)

    enc_key = RSAenc(keyPair, key)

    user_list[user_check] = [base64.b64encode(enc_key).decode("UTF-8"), enc_id.decode('UTF-8'), enc_uid.decode('UTF-8'), base64.b64encode(DS).decode("UTF-8")]
    f = open('authentication_server.json', 'w')
    json.dump(user_list,f)
    f.close()

    print("The "+type+' user has been registered.')
    print("Your patient ID is:", id)
    print("The assigned RSA keypair has been stored in: "+u_id+'.pem')


def authenticate_patient(RSAfile, id):
    if not os.path.exists('authentication_server.json'):
        print("No patient user registered")
        return
    f = open('authentication_server.json', 'r')
    user_list = json.load(f)
    f.close()

    u_id = RSAfile[:len(RSAfile)-4]
    
    if ("patient: "+u_id) not in user_list:
        print("Unauthorized access")
        return
    
    user_details = user_list["patient: "+u_id]
    enc_key = user_details[0]

    enc_key = (enc_key).encode('utf-8')
    enc_key = base64.b64decode(enc_key)

    f = open(RSAfile,'rb')
    RSAkey = f.read()
    f.close()
    keyPair = RSA.import_key(RSAkey)


    dec_key = RSAdec(keyPair, enc_key)


    auth_uid = Fernetdec(dec_key, user_details[2].encode('utf-8'))
    auth_id = Fernetdec(dec_key, user_details[1].encode('utf-8'))


    if auth_id.decode("UTF-8") == str(id) and auth_uid.decode("UTF-8") == u_id:
        print('You have been successfully authenticated as a registered user.')
        return (True, u_id)
    else:
        print('Digital signature mismatch. Access denied')
        return (False, u_id)


def authenticate_auditor(RSAfile, id):
    if not os.path.exists('authentication_server.json'):
        print("No auditor user registered")
        return
    f = open('authentication_server.json', 'r')
    user_list = json.load(f)
    f.close()

    u_id = RSAfile[:len(RSAfile)-4]
    
    if ("auditor: "+u_id) not in user_list:
        print("Unauthorized access")
        return
    
    user_details = user_list["auditor: "+u_id]
    enc_key = user_details[0]

    enc_key = (enc_key).encode('utf-8')
    enc_key = base64.b64decode(enc_key)

    f = open(RSAfile,'rb')
    RSAkey = f.read()
    f.close()
    keyPair = RSA.import_key(RSAkey)


    dec_key = RSAdec(keyPair, enc_key)

    auth_uid = Fernetdec(dec_key, user_details[2].encode('utf-8'))
    auth_id = Fernetdec(dec_key, user_details[1].encode('utf-8'))


    if auth_id.decode("UTF-8") == str(id) and auth_uid.decode("UTF-8") == u_id:
        print('You have been successfully authenticated as a registered user.')
        return (True, u_id)
    else:
        print('Digital signature mismatch. Access denied')
        return (False, u_id)


