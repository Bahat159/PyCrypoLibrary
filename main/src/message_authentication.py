from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives import poly1305
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.ciphers import algorithms


# While cryptography supports multiple MAC algorithms, 
# we strongly recommend that HMAC should be used unless you have a very specific need.
#
# For more information on why HMAC is preferred, see Use cases for CMAC vs. HMAC?



# Cipher-based message authentication codes (or CMACs) 
# are a tool for calculating message authentication codes 
# using a block cipher coupled with a secret key. 
# You can use an CMAC to verify both the integrity and authenticity of a message.
#
# A subset of CMAC with the AES-128 algorithm is described in RFC 4493.
#
# CMAC objects take a BlockCipherAlgorithm instance.

class Cipher_based_message_authentication_code:
    def __init__(self):
        self.message_to_authenticate = bytes("message to authenticate", encoding="utf8")
        self.incorrect_signature_message = bytes("an incorrect signature", encoding="utf8")
    

    def __repr__(self):
        return self
    
    def cmac_authentication(self, key, use_cmac_authenctication = True):
        if use_cmac_authenctication:
            c = cmac.CMAC(algorithms.AES(key))
            c.update(self.message_to_authenticate)
            c.finalize()
        return c
    
    # If algorithm isn’t a BlockCipherAlgorithm instance then TypeError will be raised.
    # To check that a given signature is correct use the verify() method. 
    # You will receive an exception if the signature is wrong:
    
    def check_cmac_signature(self, key, use_cmac_signature = True):
        if use_cmac_signature:
            c = cmac.CMAC(algorithms.AES(key))
            c.update(self.message_to_authenticate)
            c.verify(self.incorrect_signature_message)
        return c

# Hash-based message authentication codes (or HMACs) 
# are a tool for calculating message authentication codes 
# using a cryptographic hash function coupled with a secret key. 
# You can use an HMAC to verify both the integrity and authenticity of a message.
#
# HMAC objects take a key and a HashAlgorithm instance. 
# The key should be randomly generated bytes and is 
# recommended to be equal in length to the digest_size of the hash function chosen. 
# You must keep the key secret.
#
# This is an implementation of RFC 2104.

class Hash_based_message_authentication_codes:
    def __init__(self):
        self.signature = bytes("an incorrect signature", encoding="utf8")
        self.key = bytes('test key. Beware! A real key should use os.urandom or TRNG to generate', encoding="utf8")
        self.message_to_hash = bytes("message to hash", encoding="utf8")
    

    def __repr__(self):
        return self
    
    def hmac_message_authentication(self, use_hmac_authentication = True):
        if use_hmac_authentication:
            h = hmac.HMAC(key, hashes.SHA256())
            h.update(self.message_to_hash)
            signature = h.finalize()
        return signature
    
    def check_hmac_signature(self, signature, use_check_signature = True):
        if use_check_signature:
            h = hmac.HMAC(key, hashes.SHA256())
            h.update(self.message_to_hash)
            h_copy = h.copy() # get a copy of `h' to be reused
            h.verify(signature)
            h_copy.verify(self.signature)
        return h_copy

# Poly1305 is an authenticator that takes a 32-byte key 
# and a message and produces a 16-byte tag. 
# This tag is used to authenticate the message. 
# Each key must only be used once. 
# Using the same key to generate tags for multiple messages allows an attacker to forge tags. 
# Poly1305 is described in RFC 7539.
#
#
# Using the same key to generate tags for multiple messages allows an attacker to forge tags. 
# Always generate a new key per message you want to authenticate. 
# If you are using this as a MAC for symmetric encryption please use ChaCha20Poly1305 instead.

class Poly1305:
    def __init__(self):
        self.message_to_authenticate = bytes("message to authenticate", encoding = True)
        self.use_incorrect_tag = bytes("an incorrect tag", encoding = "utf8")
    

    def __repr__(self):
        return self

    def poly1305_authentication(self, key, use_poly1305 = True):
        if use_poly1305:
            p = poly1305.Poly1305(key)
            p.update(self.message_to_authenticate)
            p.finalize()
        return p
    
    # To check that a given tag is correct use the verify() method. 
    # You will receive an exception if the tag is wrong:

    def check_signature_tag(self, key, use_check_tag = True):
        if use_check_tag:
            p = poly1305.Poly1305(key)
            p.update(self.message_to_authenticate)
            p.verify(self.use_incorrect_tag)
        return p
    
    # A single step alternative to do sign operations. 
    # Returns the message authentication code as bytes for the given key and data.

    def alternative_sign_operation(self, key, use_alternative_operation = True):
        if use_alternative_operation:
            return poly1305.Poly1305.generate_tag(key, self.message_to_authenticate)
    
    # A single step alternative to do verify operations. 
    # Securely compares the MAC to tag, using the given key and data.

    def verify_tag(self, key, use_verify_tag = True):
        if use_verify_tag:
            return poly1305.Poly1305.verify_tag(key, self.message_to_authenticate self.use_incorrect_tag)


# Message digests (Hashing)
#
# A cryptographic hash function takes an arbitrary 
# block of data and calculates a fixed-size bit string (a digest), 
# such that different data results (with a high probability) in different digests.
#
# This is an implementation of HashContext meant to be 
# used with HashAlgorithm implementations to provide an 
# incremental interface to calculating various message digests.

class Message_digests:
    def __init__(self):
        self.message = bytes("abc", encoding="utf8")
        self.update_message = bytes("123", encoding="utf8")
    

    def __repr__(self):
        return self

    # Keep in mind that attacks against cryptographic hashes only get stronger with time, 
    # and that often algorithms that were once thought to be strong,
    # become broken. Because of this it’s important to 
    # include a plan for upgrading the hash algorithm you use over time. 
    # For more information, 
    # see Lifetimes of cryptographic hash functions.[https://valerieaurora.org/hash.html]

    def calculate_message_digest(self, use_message_digest = True):
        if use_message_digest:
            digest = hashes.Hash(hashes.SHA256())
            digest.update(self.message)
            digest.update(self.update_message)
            digest.finalize()
        return digest

# SHA-2 family
#
# SHA-224 is a cryptographic hash function from the SHA-2 family 
# and is standardized by NIST. 
# It produces a 224-bit message digest.

# BLAKE2
#
# BLAKE2 is a cryptographic hash function specified in RFC 7693. 
# BLAKE2’s design makes it immune to length-extension attacks, 
# an advantage over the SHA-family of hashes.

# SHA-3 family
#
# SHA-3 is the most recent NIST secure hash algorithm standard. 
# Despite the larger number SHA-3 is not considered to be better than SHA-2. 
# Instead, it uses a significantly different internal structure 
# so that if an attack appears against SHA-2 
# it is unlikely to apply to SHA-3. SHA-3 is significantly slower 
# than SHA-2 so at this time most users should choose SHA-2.

# SHA-1
#
# Warning
# SHA-1 is a deprecated hash algorithm that has practical known collision attacks. 
# You are strongly discouraged from using it. Existing applications should strongly consider moving away.
#
# SHA-1 is a cryptographic hash function standardized by NIST. 
# It produces an 160-bit message digest. 
# Cryptanalysis of SHA-1 has demonstrated that it is vulnerable to practical collision attacks, 
# and collisions have been demonstrated.

# MD5
#
# Warning
# MD5 is a deprecated hash algorithm that has practical known collision attacks. 
# You are strongly discouraged from using it. Existing applications should strongly consider moving away.
#
# MD5 is a deprecated cryptographic hash function. 
# It produces a 128-bit message digest and has practical known collision attacks.

# SM3
#
# SM3 is a cryptographic hash function standardized 
# by the Chinese National Cryptography Administration in GM/T 0004-2012. 
# It produces 256-bit message digests. 
# (An English description is available at draft-oscca-cfrg-sm3-02.) 
# This hash should be used for compatibility purposes where required 
# and is not otherwise recommended for use.
