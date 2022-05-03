

from query import decrypt_audit_log
from hashlib import sha256
import csv
import os
from datetime import datetime

def hashFunction(filename):
    cipher = sha256()
    with open(filename, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            cipher.update(byte_block)
    #hashed = sha256(raw.encode("UTF-8")).hexdigest()
    return cipher.hexdigest()

def report(u_id, id, now, line, og, new):
    out = "Tamper attempt on "+str(now)+" by User: "+str(u_id)+" with ID: "+str(id)+" in the audit log.\nThey tried to change line "+str(line)+" with entry "+str(og)+ " to "+str(new)+"."

    return out


def check_integrity(id, u_id):

    print('We will now walkthrough a scenorio where system detects changes made to audit log and report it')
    
    decrypt_audit_log()

    list_audit= []
    f = open('temp_audit.csv', 'r')
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        list_audit.append(row)
    f.close()

    f= open('og_audit_log.txt', 'r')
    audit_log_hash = f.read()
    f.close()

    print("Instance of Audit Log created")
    if audit_log_hash == hashFunction('temp_audit.csv'):
        print('Hashes match. We will proceed')
    else:
        print('Hash mismatch. Original file tampered')
    
    print('Following is the data from the Audit Log instance created')
    for row in list_audit:
        print(','.join(row))
    
    line = int(input("Select a line number between 1-"+str(len(list_audit))+' to edit: '))
    print("Following line will be edited:", list_audit[line])
    og = list_audit[line]
    edit_input = str(input("Enter the new value for the line: "))
    list_audit[line] = [edit_input]

    with open('temp_audit.csv', 'w', newline='') as x:
        f_writer = csv.writer(x, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for ele in list_audit:
            f_writer.writerow(ele)
    
    now = datetime.now()
    now = str(now).replace(':',';')

    if audit_log_hash != hashFunction('temp_audit.csv'):
        f = open('Tamper_Attempt_User_'+str(u_id)+'_ID_'+str(id)+'_'+str(now)+'.txt', 'w')
        f.write(report(u_id,id,now, line, og, edit_input))
        print('FILE TAMPERING DETECTED. ATTEMPT LOGGED IN FILE Tamper_Attempt_User_'+str(u_id)+'_ID_'+str(id)+'_'+str(now)+'.txt')
    else:
        print('Hash match. Original file untampered')

    os.remove('temp_audit.csv')





