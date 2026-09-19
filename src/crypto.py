from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization,hashes
from cryptography.hazmat.primitives.asymmetric import padding
from config import MYNODE

private_key = serialization.load_ssh_private_key(
    open(f"keys/{MYNODE}","rb").read(),
    backend=default_backend(),
    password=None
)

def decryptRSA(c: bytes):
    return private_key.decrypt(
        c,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )   
    )


def encryptRSA(k,m: bytes):
    return k.encrypt(
        m,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )   
    )


def decryptAES(k,c: bytes):
    return AESGCM(k).decrypt(k, c, None)


def encryptAES(k,m: bytes):
    return AESGCM(k).encrypt(k, m, None)

