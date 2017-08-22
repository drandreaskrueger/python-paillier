'''
Created on 16 Aug 2017

@summary:   tests for the homomorphic encryption wrapper,
            useful for checking the backport to python 2.7

@author: github.com/drandreaskrueger  (electron.org.uk)
            
@quickstart: 
            source env/Electron/bin/activate
            pip install pytest 
            pytest -k homomorphic_encryption


'''
import pytest
import numpy 
import sys
import pickle
import os


from phe import paillier
from homomorphic_encryption import HE_generate_keypair, HE_encrypt_data, \
                                   HE_encrypt_single, HE_decrypt, \
                                   HE_allPublicKeys, \
                                   HE_serialize, HE_deserialize

def test_dummy():
    assert 42 != 23
    
    
def test_HE_generate_keypair():
    kp = HE_generate_keypair()
    assert len(kp) == 2
    publicKey, privateKey = kp
    assert type(publicKey) == paillier.PaillierPublicKey
    assert type(privateKey) == paillier.PaillierPrivateKey


def test_HE_encrypt_data():
    public_key, _ = HE_generate_keypair()
    cleartext = [42.0,]
    ciphertext = HE_encrypt_data(cleartext, public_key)
    assert type(ciphertext) == numpy.ndarray
    assert type(ciphertext[0]) == paillier.EncryptedNumber


def test_HE_decrypt():
    public_key, private_key = HE_generate_keypair()
    cleartexts = [42.0, 23.0, -1.0]
    ciphertexts = HE_encrypt_data(cleartexts, public_key)
    for i, ciphertext in enumerate(ciphertexts):
        ciphertext_decrypted = HE_decrypt(ciphertext, private_key)
        assert ciphertext_decrypted==cleartexts[i] 
        
def test_HE_add_encrypted_numbers():
    public_key, private_key = HE_generate_keypair()
    cleartexts = [42.0, 23.0]
    ciphertexts = HE_encrypt_data(cleartexts, public_key)
    ciphertexts = list(ciphertexts)
    
    ciphertextsum = ciphertexts[0] + ciphertexts[1]
    ciphertext_decrypted = HE_decrypt(ciphertextsum, private_key)
    assert ciphertext_decrypted == sum(cleartexts)
        

def test_HE_multiply_encrypted_number_with_unencrypted_scalar():
    public_key, private_key = HE_generate_keypair()
    cleartext = 42.0
    ciphertext = public_key.encrypt(cleartext)
    scalar = 2.0
    result = ciphertext * scalar 
    result_decrypted = HE_decrypt(result, private_key)
    assert result_decrypted == cleartext * scalar
    

def make_ListOfNumbersWithSeveralKeys():
    cleartexts=[42.0, 23.0]
    ciphertexts=[]
    for cleartext in cleartexts:
        public_key, private_key = HE_generate_keypair()
        ciphertext = HE_encrypt_single(cleartext, public_key)
        ciphertexts.append(ciphertext)
    return ciphertexts


def test_HE_allPublicKeys():
    ciphertexts = make_ListOfNumbersWithSeveralKeys()
    pks = HE_allPublicKeys(ciphertexts)
    assert len(pks) == 2
    
    
@pytest.mark.parametrize("withKey", [True, False])
def test_HE_serialize_deserialize_array(withKey):
    public_key, private_key = HE_generate_keypair()
    
    cleartext=[42.0, 23.0]
    ciphertext = HE_encrypt_data(cleartext, public_key)
    
    give_public_key = public_key if withKey else None
    serialized = HE_serialize(ciphertext, give_public_key)
     
    pk, deserialized = HE_deserialize(serialized)
    assert public_key == pk
    
    for i, d in enumerate(deserialized):
        before = HE_decrypt(list(ciphertext)[i], private_key)
        assert HE_decrypt(d, private_key) == before
        assert before == cleartext[i]


def test_HE_serialize_fails_for_different_keys():
    ciphertexts = make_ListOfNumbersWithSeveralKeys()
    
    with pytest.raises(ValueError):
        serialized = HE_serialize(ciphertexts, public_key=None)
    

    
