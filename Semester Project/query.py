#!/usr/bin/env python3

import os.path
import sys
from Crypto import Random
from Crypto.Cipher import  PKCS1_OAEP
from Crypto.PublicKey import RSA
import os
from cryptography.fernet import Fernet
import csv
from datetime import datetime

def patient_query(id):

    decrypt_audit_log()
    query_helper_patient(id)
    os.remove('temp_audit.csv')

def auditor_query(id):
    decrypt_audit_log()
    query_helper_auditor(id)
    os.remove('temp_audit.csv')

def decrypt_audit_log():
    with open('audit_log.csv.enc', 'rb') as f:
        ciphertext = f.read()
        
    with open('adl.csv.key', 'rb') as f:
        enc_key = f.read()

    f = open('audit_log_keypair.pem', 'r')
    RSAkey = RSA.import_key(f.read())

    decryptor = PKCS1_OAEP.new(RSAkey)
    dec_key = decryptor.decrypt(enc_key)
    
    fernet = Fernet(dec_key)

    decrypted = fernet.decrypt(ciphertext)

    with open('temp_audit.csv', 'wb') as f:
        f.write(decrypted)


def query_helper_patient(id):
    csvfile = open('temp_audit.csv', 'r')
    header = next(csvfile).strip("\n").split(",")
    reader = csv.reader(csvfile)
    results = filter(lambda row: row[1] == str(id), reader)
    
    now = datetime.now()
    now = str(now).replace(':',';') 

    with open('patient_'+str(id)+'_query_'+str(now)+'.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)
        for result in results:
            writer.writerow(result)
    csvfile.close()
    print('Created file: '+'patient_'+str(id)+'_query_'+str(now)+'.csv')

def query_helper_auditor(id):
    id_list = str(input("Please enter the patient ID/s you want to access (separated with a space): "))
    csvfile = open('temp_audit.csv', 'r')
    header = next(csvfile).strip("\n").split(",")
    reader = csv.reader(csvfile)
    results = filter(lambda row: row[1] in id_list, reader)
    
    now = datetime.now()
    now = str(now).replace(':',';')

    with open('auditor_'+str(id)+'_query_'+str(now)+'.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)
        for result in results:
            writer.writerow(result)
    
    csvfile.close()
    print('Created file: '+'auditor'+str(id)+'_query_'+str(now)+'.csv')
