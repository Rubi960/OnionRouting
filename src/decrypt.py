from crypto import decryptAES, decryptRSA
from prints import finalMessage
from config import KEYLEN

def extractHop(text: bytes):
    return text[:5].strip(b'\x00').strip(b'0'), text[5:]

def decrypt(text):
    cipherKey = text[:KEYLEN]
    cipherText = text[KEYLEN:]

    key = decryptRSA(cipherKey)
    return decryptAES(key,cipherText)

def decapsule(capsule):
    decipher = decrypt(capsule)
    hop, msg = extractHop(decipher)
    hop = hop.decode('ascii')

    if hop == 'end':
        source, msg = extractHop(msg)
        finalMessage(source.decode('ascii'),msg.decode('ascii'))
        return None, None
    else:
        return hop, msg