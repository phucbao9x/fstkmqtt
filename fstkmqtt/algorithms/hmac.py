try: 
    import hmac as hm
    import hashlib as hl
    import binascii as basi
except: 
    print('Run command after you go to the the next stop:\n>>pip install -r requirement.txt')
    exit(0)

def hmacsha256(key : str, msg: str):
    key= basi.unhexlify(key)
    msg = msg.encode()
    return hm.new(key, msg, hl.sha256).hexdigest()
    
def merginhmacsha256(key : str, msgl: list[str]):
    result = ''
    for msg in msgl:
        key= basi.unhexlify(key)
        msg = msg.encode()
        result += hm.new(key, msg, hl.sha256).hexdigest()
    return result
    
hmac = hm.HMAC