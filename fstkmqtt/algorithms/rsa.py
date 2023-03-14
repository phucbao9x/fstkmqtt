try:
    from Crypto.PublicKey import RSA
    from Crypto import Random
    from Crypto.Cipher import PKCS1_OAEP
    from datetime import datetime as dtt
    from os import path
except: 
    exit(0)
try: 
    from ..typings.directory import strOrBytesPath
    from ..typings.directory import t
except: 
    strOrBytesPath = str|bytes
    import typing as t

def decrypto(
        datafile : strOrBytesPath, 
        filekey: strOrBytesPath, 
        outfile : strOrBytesPath) -> bytes:
    f = open(filekey, 'rb')
    private_key_pem_data = f.read()
    f.close()
    f = open(datafile, 'rb')
    data = f.read()
    f.close()
    rsakey : RSA.RsaKey = RSA.import_key(private_key_pem_data)
    key = PKCS1_OAEP.new(rsakey)
    buffer = 16
    new = b''
    while True:
        data = f.read(buffer)
        new += key.encrypt(data)
        if len(data) < buffer: break
    f.close()

    f = open(outfile, 'wb')
    f.write(new)
    f.close()
    return new

def encrypto(
        datafile: strOrBytesPath,
        filekey: strOrBytesPath,
        outfile : strOrBytesPath) -> int:
    f = open(filekey, 'rb')
    publish_key_pem = f.read()
    f.close()
    rsakey : RSA.RsaKey = RSA.import_key(publish_key_pem)
    rsakey = rsakey.publickey()
    key = PKCS1_OAEP.new(rsakey)
    buffer = 16
    f = open(datafile, 'rb')
    new = b''
    while True:
        data = f.read(buffer)
        new += key.encrypt(data)
        if len(data) < buffer: break
    f.close()
    f = open(outfile, 'wb')
    f.write(new)
    f.close()
    return new

def createPEM(
        bits: int = 2048, 
        ranfunc : t.Callable = Random.new().read, 
        exponent_public : int = 2**16+1, 
        privatefilename: str | None= None,
        publicfilename: str|None = None,
        parentdir : str | None= '.'):
    now = dtt.now()
    privatefilename = (privatefilename + '.pem') if privatefilename else f'pri_{now.day}-{now.month}-{now.year}_{now.hour}-{now.minute}-{now.second}.pem'
    publicfilename = (publicfilename + '.pem') if publicfilename else f'pub_{now.day}-{now.month}-{now.year}_{now.hour}-{now.minute}-{now.second}.pem'
    parentdir = parentdir if parentdir else '.'
    random_generator = Random.new().read
    rsakey = RSA.generate(2048, random_generator)
    key = rsakey.public_key().exportKey()
    key2 = rsakey.exportKey()
    f = open(path.join(parentdir, publicfilename), 'wb')
    f.write(key)
    f.close()
    f = open(path.join(parentdir, privatefilename), 'wb')
    f.write(key2)
    f.close()

def test():
    createPEM(privatefilename='private', publicfilename='public')
    encrypto('test.txt', 'public.pem', 'testen.txt')
    decrypto('testen.txt', 'private.pem', 'testde.txt')