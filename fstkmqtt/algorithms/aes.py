try:
    from .sha import (
        sha1,
        sha224,
        sha256,
        sha384,
        sha3_224,
        sha3_256,
        sha3_512,
        sha512
    )
    
except:
    from hashlib import (
        sha1,
        sha224,
        sha256,
        sha384,
        sha3_224,
        sha3_256,
        sha3_512,
        sha512
    )
finally:
    import base64
    from Crypto import Random
    from Crypto.Cipher import AES

class AESCipher(object):
    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = sha256(key.encode()).digest()

    def encrypt(self, raw : bytes):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs).encode()

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]