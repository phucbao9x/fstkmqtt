try: 
    import hashlib
    import hmac
except: 
    print('Run command after you go to the the next stop:\n>>pip install -r requirement.txt')
    exit(0)
    
sha1 = hashlib.sha1
md5 = hashlib.md5
sha224 = hashlib.sha224
sha256 = hashlib.sha256
sha384 = hashlib.sha384
sha512 = hashlib.sha512
sha3_224 = hashlib.sha3_224
sha3_256 = hashlib.sha3_256
sha3_512 = hashlib.sha3_512