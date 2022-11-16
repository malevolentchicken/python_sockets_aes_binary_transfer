# server.py

import socket                  
import sys
from Crypto.Cipher import AES
from Crypto import Random
import hashlib


# ////////////////////////////////////////////// Read in the file to be transferred and encrypt with AES. //////////////////////////////////////////////

filename = sys.argv[1] 
with open(filename, 'rb') as infile:
	plaintext = infile.read()

encryption_password = "SecretKey123" 

# Hashed in order to meet AES length requirements.
key = hashlib.sha256(encryption_password.encode()).digest() 

plaintext = plaintext + b"\0" * (AES.block_size - len(plaintext) % AES.block_size)
iv = Random.new().read(AES.block_size)
cipher = AES.new(key, AES.MODE_CBC, iv)
ciphertext = iv + cipher.encrypt(plaintext) 

with open(filename + ".enc", 'wb') as outfile: 
        outfile.write(ciphertext)

# ////////////////////////////////////////////// Create a socket to listen on and transfer file over. //////////////////////////////////////////////

port = 4444   					
s = socket.socket()             
host = socket.gethostname()     
s.bind((host, port))            
s.listen(5)                     

print ('Server Awaiting Connections')

while True:
    conn, addr = s.accept()     
    print ('Got connection from', addr)
    
    f = open(filename + ".enc",'rb')
    l = f.read(1024)
    while (l):
       conn.send(l)
       print('Sent ',repr(l))
       l = f.read(1024)
    f.close()

    print('Transfer Complete')
    conn.close()
