from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pubkeys import getPubkey
from crypto import encryptAES, encryptRSA

def formatHop(node: bytes):
    return b'\x00'* (5 - len(node)) + node

def encrypt(pubK, k, m):
    return encryptRSA(pubK,k) + encryptAES(k,m)

def encapsule(pubKey, msg: bytes):
    key = AESGCM.generate_key(bit_length=128)

    return encrypt(pubKey, key, msg)

def getEncrypted(source: bytes, route, msg: bytes):
    inversedRoute = route[::-1]

    # First packet
    lastHop: bytes = formatHop(b'end')    
    for node in inversedRoute:
        msg = encapsule(getPubkey(node),lastHop + formatHop(source) + msg)
        lastHop = b''
        source = node.encode('ascii')
    
    return route[0], msg