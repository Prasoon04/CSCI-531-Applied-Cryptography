# genkeys.py
  The program takes the username input from the command line, and it generates the public and private key pairs. The program calls generate_keys function which generates p and q pair for the RSA. The random key is generated within the specified range using the keysize for the RSA. The p and q are then tested for prime and go through rabin miller test to check the correctness. If the test fails, then a new random number is generated until the prime test is passed. The rabin miller incorporates finding r and s such that (n-1) = r*(2^s) where r is odd.
  The program then calculates N and φ(N) value for the RSA key pair generation. A suitable e is calculated by performing GCD between e and φ(N) until we reach GCD = 1. After this, the script finds the modular inverse to calculate d for the calculation.

![alt text](https://github.com/Prasoon04/CSCI-531-Applied-Cryptography/blob/main/Programming%20Assignment%202/Screenshot/1.png)
<br>
Python genkeys.py alice<br>
<br/>

![alt text](https://github.com/Prasoon04/CSCI-531-Applied-Cryptography/blob/main/Programming%20Assignment%202/Screenshot/2.png)<br>
Python genkeys.py bob

# crypt.py
The program takes in user input from command line to determine whether an encryption or decryption needs to be done.
1.	If encryption is selected, the program generates a random byte of 16 bytes. The encoded bytes are then converted to int, and AES Cipher class is called on it. The initialization creates an instance of the AES key. The AES key is then encrypted using user’s public key. Public key pair (N,e) are extracted from the file generated from genkeys,py and the AES key is encrypted. The program then encrypts the message. It reads the message and encodes the after padding it. As CBC mode is used, so an IV is generated with 16-byte size. The AES key is then encoded and a sha256 digest is created. The encoded key and IV are then used to encrypt the message. The IV along with the cipher text are further encoded. The ciphertext along with encrypted AES key using RSA are saved in a file.
2.	If decryption is selected, the program calls the AES Cipher class and runs the decrypt function. Private key pair (N,d) are extracted from the supplied private key file. The encrypted key extracted from the encrypted message is then decrypted using RSA. Sha256 is used to generate a digest for added security and the key is decoded. The IV is extracted and then decryption takes place using CBC mode. The clear text is printed in the file.<br>

![alt text](https://github.com/Prasoon04/CSCI-531-Applied-Cryptography/blob/main/Programming%20Assignment%202/Screenshot/3.png)<br>
cat (type for Windows) message.txt<br>
<br/>

![alt text](https://github.com/Prasoon04/CSCI-531-Applied-Cryptography/blob/main/Programming%20Assignment%202/Screenshot/4.png)<br> 
Python crypt.py -e bob.pub message.txt message.cip

![alt text](https://github.com/Prasoon04/CSCI-531-Applied-Cryptography/blob/main/Programming%20Assignment%202/Screenshot/5.png)<br>
cat (type for Windows) message.cip<br>
<br/>

![alt text](https://github.com/Prasoon04/CSCI-531-Applied-Cryptography/blob/main/Programming%20Assignment%202/Screenshot/6.png)<br>
Python crypt.py -d bob.prv message.cip dec_message.txt<br>
<br/>

![alt text](https://github.com/Prasoon04/CSCI-531-Applied-Cryptography/blob/main/Programming%20Assignment%202/Screenshot/7.png)<br>
cat (type for Windows) dec_message.txt<br>
<br/>

![alt text](https://github.com/Prasoon04/CSCI-531-Applied-Cryptography/blob/main/Programming%20Assignment%202/Screenshot/8.png)<br>
cat (type for Windows) message2.txt<br>
<br/>

![alt text](https://github.com/Prasoon04/CSCI-531-Applied-Cryptography/blob/main/Programming%20Assignment%202/Screenshot/9.png)<br>
Python crypt.py -e alice.pub message2.txt message2.cip<br>
<br/>

![alt text](https://github.com/Prasoon04/CSCI-531-Applied-Cryptography/blob/main/Programming%20Assignment%202/Screenshot/10.png)<br> 
cat (type for Windows) message2.cip<br>
<br/>

![alt text](https://github.com/Prasoon04/CSCI-531-Applied-Cryptography/blob/main/Programming%20Assignment%202/Screenshot/11.png)<br>
Python crypt.py -d alice.prv message2.cip dec)message2.txt<br>
<br/>

![alt text](https://github.com/Prasoon04/CSCI-531-Applied-Cryptography/blob/main/Programming%20Assignment%202/Screenshot/12.png)<br>
cat (type for Windows) dec_message2.txt



 


