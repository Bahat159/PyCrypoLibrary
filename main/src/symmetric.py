import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.modes import CBC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


# Symmetric encryption
#
# Symmetric encryption is a way to encrypt or hide the contents 
# of material where the sender and receiver both use the same secret key. 
# Note that symmetric encryption is not sufficient for most applications 
# because it only provides secrecy but not authenticity. 
# That means an attacker can’t see the message but an attacker 
# can create bogus messages and force the application to decrypt them. 
# In many contexts, a lack of authentication on encrypted messages can result in a loss of secrecy as well.
#
# For this reason it is strongly recommended to combine encryption 
# with a message authentication code, such as HMAC, 
# in an “encrypt-then-MAC” formulation as described by Colin Percival. 
# cryptography includes a recipe named Fernet (symmetric encryption) 
# that does this for you. To minimize the risk of security issues 
# you should evaluate Fernet to see if it fits your needs before implementing anything using this module.

# Example Usage
#class_object = symmertic_Encryption()
#encrypt = class_object.do_AES_encryption()
#decrypt = class_object.do_AES_decryption(encrypt)
#
#print(encrypt)
# b'\x19\x0c\x93\x1c\xffx\x8d*zv\xe7\x97\x12\xb3\xed\xad'
#
#print(decrypt)
# b'a secret message'


class symmertic_Encryption:
    # Cipher objects combine an algorithm such as AES with a mode like CBC or CTR. 
    # A simple example of encrypting and then decrypting content with AES is:

    def __init__(self):
        self.key             = os.urandom(int('32'))
        self.chahcha_nonce   = os.urandom(int('16'))
        self.key_length      = os.urandom(int('32'))  # (32, 128, 192, 156)
        self.key_iv          = os.urandom(int('16'))
        self.AES_cipher      = Cipher(algorithms.AES(self.key_length), modes.CBC(self.key_iv))
        self.secret_message  = bytes("a secret message", encoding = "utf8")
        self.associated_data = bytes("authenticated but not encrypted payload", encoding="utf8")
        self.plaintext_data  = bytes("a secret message! from the author. What if it is a file? \nAuthor: Busari Habibullah.\nTest Date: January 26, 2022\nCompany name: Sandcroft software,", encoding="utf8")
    
    def __repr__(self):
        return self
    
    def __str__(self):
        return self
    
    def do_AES_encryption(self):
        encryptor = self.AES_cipher.encryptor()
        ct = encryptor.update(self.secret_message) + encryptor.finalize()
        return ct
    
    def do_AES_decryption(self, ct):
        decryptor = self.AES_cipher.decryptor()
        return decryptor.update(ct) + decryptor.finalize()
    

    # ChaCha Algorithm

    def do_chacha_encryption(self, key, use_chacha_encryptor = True):
        if use_chacha_encryptor:
            algorithm = algorithms.ChaCha20(key, self.chahcha_nonce)
            cipher = Cipher(algorithm, mode=None)
            encryptor = cipher.encryptor()
            ct = encryptor.update(self.secret_message)
        return ct
    
    def do_chacha_decryption(self, ct, use_chacha_decryptor = True):
        if use_chacha_decryptor:
            algorithm = algorithms.ChaCha20(key, self.chahcha_nonce)
            cipher = Cipher(algorithm, mode=None)
            decryptor = cipher.decryptor()
        return decryptor.update(ct)
    
    
    # Modes
    #
    # CBC (Cipher Block Chaining) is a mode of operation for block ciphers. 
    # It is considered cryptographically strong.

    def cbc_mode_construction(self, use_cbc_mode = True):
        if use_cbc_mode:
            iv = os.urandom(16)
            mode = CBC(iv)
        return mode

    # If you are encrypting data that can fit into memory 
    # you should strongly consider using AESGCM instead of this.
    #
    # When using this mode you must not use the decrypted data 
    # until the appropriate finalization 
    # method (finalize() or finalize_with_tag()) has been called. 
    # GCM provides no guarantees of ciphertext integrity until decryption is complete.
    #
    # GCM (Galois Counter Mode) is a mode of operation for block ciphers. 
    # An AEAD (authenticated encryption with additional data) mode 
    # is a type of block cipher mode that simultaneously 
    # encrypts the message as well as authenticating it. 
    # Additional unencrypted data may also be authenticated. 
    # Additional means of verifying integrity such as HMAC are not necessary.
    #
    #
    # GCM Use case
    #
    # class_object = symmertic_Encryption()
    # cipher_text, encryptor_tag = class_object.do_gcm_encrypt()
    # print(class_object.do_gcm_decrypt(cipher_text, encryptor_tag))
    
    def do_gcm_encrypt(self, use_gcm_encryptor = True):
        if use_gcm_encryptor:
            encryptor = Cipher(algorithms.AES(self.key),modes.GCM(self.key_iv),backend=default_backend()).encryptor()
            encryptor.authenticate_additional_data(self.associated_data)
            ciphertext = encryptor.update(self.plaintext_data) + encryptor.finalize()
        return (ciphertext, encryptor.tag)
    
    def do_gcm_decrypt(self, ciphertext, encryptor_tag, use_gcm_decryptor = True):
        if use_gcm_decryptor:
            decryptor = Cipher(algorithms.AES(self.key),modes.GCM(self.key_iv, encryptor_tag),backend=default_backend()).decryptor()
            decryptor.authenticate_additional_data(self.associated_data)
            return decryptor.update(ciphertext) + decryptor.finalize()
