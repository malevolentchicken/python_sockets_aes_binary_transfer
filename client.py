# client.py

import socket       
from Crypto.Cipher import AES
from Crypto import Random
import hashlib


encryption_password = "SecretKey123" 
key = hashlib.sha256(encryption_password.encode()).digest() # Hashed in order to meet AES length requirements.            

# ////////////////////////////////////////////// Create a socket to listen on and transfer file over. //////////////////////////////////////////////

s = socket.socket()             
host = socket.gethostname()     # Get local machine name. Replace this with an IP Address if you are going over a network.
port = 4444                    

s.connect((host, port))

with open('received_file.enc', 'wb') as f:    
    while True:
        print ("\n ------- Receiving Data  ------- \n")
        data = s.recv(1024)
        print ("data=" + str(data))
        if not data:
            break        
        f.write(data)

f.close()
print('\nFile Retrieved')

s.close()
print('Connection Closed')

# ////////////////////////////////////////////// Read in the file received and decrypt. //////////////////////////////////////////////

with open('received_file.enc', 'rb') as encfile:
        ciphertext = encfile.read()

iv = ciphertext[:AES.block_size]
cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = cipher.decrypt(ciphertext[AES.block_size:])
decrypted = plaintext.rstrip(b"\0")

with open('received_file', 'wb') as fileout:
        fileout.write(decrypted)
