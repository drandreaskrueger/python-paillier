"""

@summary: simple wrappers for only those phe.paillier functions 
          that we need

@author: github.com/drandreaskrueger  (electron.org.uk)

"""

# sudo apt-get install python3-dev libmpfr-dev libmpc-dev
# pip install phe

from phe import paillier  # for documentation see:                                 
# https://github.com/n1analytics/python-paillier/blob/master/phe/paillier.py

import numpy as np
import pickle
import json


# keys

def HE_generate_keypair():
    """generating keys for partially homomorphic Paillier scheme"""
    kp = paillier.generate_paillier_keypair()           
    return kp
    
    
# encrypt array, or single number
    
def HE_encrypt_data(cleartextarray, public_key):
    """encrypt usage data for a specific energy user"""
    
    # makes a function for applying to np_array:
    encrypt = np.vectorize(public_key.encrypt)
    # be patient, takes time:
    ciphertextarray = encrypt(cleartextarray)
    return ciphertextarray                            
    
def HE_encrypt_single(cleartext, public_key):
    """encrypt a single number"""
    # be patient, takes time:
    ciphertext = public_key.encrypt(cleartext)
    return ciphertext                            


# decrypt single number
    
def HE_decrypt(ciphertext, private_key):
    """decryption of homomorphically encrypted data"""
    cleartext = private_key.decrypt(ciphertext)
    return cleartext

# intended to handle lists of encr numbers with the same key:

def HE_allPublicKeys(encrypted_number_list):
    """
    Extract all public keys from list.
    Useful: if len(result) == 1 then all encrypted with same key    
    """
    pks = [x.public_key for x in encrypted_number_list]
    pks = list(set(pks)) # make unique
    return pks


# make into / get out-of   
#                        storable / transferable object (JSON)   

def HE_serialize(encrypted_number_list, public_key=None):
    """
    Prepares an array of encrypted numbers to be sent/stored/whatever.
    
    You can save time by giving public_key, but then be aware that it will 
    automatically be assumed that all numbers were encrypted with the same key.
    
    (Not passing a public_key causes all keys to be checked to be identical!)
    """

    if not public_key:
        public_keys = HE_allPublicKeys(encrypted_number_list)
        if len(public_keys)>1:
            raise ValueError("only serialize list of numbers encrypted with SAME key!")
        public_key = public_keys[0] 
    
    enc_with_one_pub_key = {}
   
    # example code in phe.paillier docs not 100% correct:
    #enc_with_one_pub_key['public_key'] = {'g': public_key.g,
    #                                      'n': public_key.n}
    
    enc_with_one_pub_key['public_key'] = {'n': public_key.n}
    
    enc_with_one_pub_key['encrypted_numbers'] = [
        (str(x.ciphertext()), x.exponent) for x in encrypted_number_list
        ]
    serialised = json.dumps(enc_with_one_pub_key)
    return serialised 
    

def HE_deserialize(received_dict_JSON):
    """take JSON and extract public_key and array of encrypted numbers"""
    
    received_dict = json.loads(received_dict_JSON)
    
    pk = received_dict['public_key']
    public_key_rec = paillier.PaillierPublicKey(n=int(pk['n']))
    
    enc_nums_rec = [
        paillier.EncryptedNumber(public_key_rec, int(x[0]), int(x[1]))
        for x in received_dict['encrypted_numbers']
        ]
    
    return public_key_rec, enc_nums_rec 


