import os
from ..connect import connect as con
from ...typings import strOrBytesPath
from ...supported.detecttype import istype
from ...exceptions import MissingDataException
from random import (
    choices
)

from ..sqlite.sqliteconnect import sqliteconnect

from ...algorithms.rsa import (
    encrypto,
    decrypto
)
from ...algorithms.aes import (
    AESCipher
)

from zlib import (
    compress as comp,
    decompress as decomp
)

import subprocess

import string

import sys

def defaultpath():
    if sys.platform == 'win32': return 'C:/ProgramData/fstkmqtt_warehouse'
    else: return "./user/data/fstkmqtt_warehouse"

def defaultpathrsa():
    if sys.platform == 'win32': return 'C:/ProgramData/RSA_key'
    else: return "./user/data/RSA_key"

defaultlengthname = 30

class timeline:
    # day-month-year
    date = '%d-%d-%d'
    #quarter-year
    quarterly = '%d-%d'
    # month - year
    monthly = '%d-%d'

class warehouseconnect(con):
    def __init__(self):
        self.__path__ = None
        self.__timeline__ = timeline.date
        self.__nameproject__ = None
        self.__password__ = None
        self.__privatekey__ = None
        self.__publickey__ = None
        self.__fmt__ = None

    def config(self, info: tuple,**options):
        self.__path__  = options.pop('tmp_path', self.__path__)
        if not self.__path__: 
            self.__path__ = defaultpath()
        if not os.path.isdir(self.__path__): os.mkdir(self.__path__)

        self.__password__ = options.pop('password', '')

        self.__privatekey__ = options.pop('keyfile', f'{defaultpathrsa()}/pri')
        self.__publickey__ = options.pop('pubfile', f'{defaultpathrsa()}/pub')

        self.__isrsa__ = options.pop('isrsa', False)
        self.__isaes__ = options.pop('isase', False)

        self.__timeline__ = options.pop('timeline', self.__timeline__)

        self.__nameproject__ = options.pop('nameproject', None)

        if not self.__nameproject__: raise MissingDataException

        self.__info__ = info

        self.__nowpath__ = os.path.abspath(os.path.join(self.__path__, self.__nameproject__, *[str(i) for i in self.__info__]))

        os.makedirs(self.__nowpath__, exist_ok=True)

        self.__ext__ = '.fstkmqttdb0000'

        if len(os.listdir(self.__nowpath__)):
            self.__isnew__ = False
            tmp_n = os.listdir(self.__nowpath__)[0]
            self.__file__ = os.path.join(self.__nowpath__, tmp_n)
            self.__namefile__ = tmp_n.split('.', 1)[0]
            with open(self.__file__ , 'rb') as f:
                tmp = f.read()
                if len(tmp) == 0: self.__isnew__ = True
        else:
            self.__namefile__ = ''.join(choices(population=string.ascii_letters + string.digits, k=defaultlengthname))
            self.__file__  = os.path.join(self.__nowpath__, f'{self.__namefile__}{self.__ext__}')
            f = open(self.__file__, 'x')
            f.close()
            self.__isnew__ = True

        self.__connection__ = None

        self.__isconnect = False

        self._tmp_file_ = None

    @property
    def pathtofile(self):
        return self.__file__

    def connect_new_file(self, base, namefiledb):
        tmp_file = os.path.join(base, 'tmp_' + namefiledb + '.db')
        tmp_file = os.path.join(base, tmp_file)
        try: open(tmp_file, 'x').close()
        except: pass
        subprocess.check_call(["attrib","+H",tmp_file])
        self.__connection__ = sqliteconnect()
        self.__connection__.config(database=tmp_file)
        self.__connection__.connect()
        self._tmp_file_ = tmp_file

    def _connect_old_file(self, base, namefiledb):
        tmp_file = os.path.join(base, 'tmp_' + namefiledb + '.db')
        tmp_file = os.path.join(base, tmp_file)
        self._tmp_file_ = tmp_file
        dbfile = os.path.join(base, f'{namefiledb}{self.__ext__}')
        # Read
        f = open(dbfile, 'rb')
        data_dbfile = f.read()
        f.close()
        # Decomp
        data_dbfile = decomp(data_dbfile)
        # Decrypto
        if self.__isaes__:
            k = AESCipher(self.__password__)
            data_dbfile = k.decrypt(data_dbfile)

            tmp_dbfile = dbfile.replace(self.__ext__, '')
            f = open(tmp_dbfile, 'wb')
            f.write(data_dbfile)
            f.close()
            subprocess.check_call(["attrib","+H",tmp_dbfile])
        if self.__isrsa__:
            decrypto(tmp_dbfile, self.__privatekey__, tmp_file)
            subprocess.check_call(["attrib","+H",tmp_file])
        if not os.path.isfile(tmp_file):
            with open(tmp_file, 'xb') as f: f.write(data_dbfile)
        #Connect
        self.__connection__ = sqliteconnect()
        self.__connection__.config(database=tmp_file)
        self.__connection__.connect()

    def connect(self, password : str | None = None):
        self.__password__ = password if password else self.__password__
        if self.__isnew__:
            self.connect_new_file(self.__nowpath__, self.__namefile__)
        else:
            self._connect_old_file(self.__nowpath__, self.__namefile__)
        self.__isconnect = True

    def disconnect(self):
        self.__connection__.disconnect()
        # Encrypto
        data = b''
        with open(self._tmp_file_, 'rb') as f: data = f.read()
        if self.__isrsa__:
            encrypto(self._tmp_file_, self.__publickey__, self.__file__.replace(self.__ext__, ''))
            subprocess.check_call(["attrib","+H",os.path.abspath(self.__file__.replace(self.__ext__, ''))])
            with open(self.__file__.replace(self.__ext__, ''), 'rb') as f: data = f.read()
            os.remove(self.__file__.replace(self.__ext__, ''))
        
        if self.__isaes__:
            k = AESCipher(self.__password__)
            data = k.encrypt(data)
            
        os.remove(self._tmp_file_)

        # Compression
        data = comp(data)
        print(self.__file__)
        f = open(self.__file__, 'wb')
        f.write(data)
        f.close()

        self.__isconnect = False

    def reconnect(self, info: tuple,**options):
        self.config(info, **options)
        if self.__isconnect: self.disconnect()
        self.connect()

    def execute(self, fmt, data: tuple, iscommit : bool = False, isdata: bool = False):
        return self.__connection__.execute(fmt, data, iscommit, isdata)

    def executemany(self, fmt, *data, iscommit : bool = False, isdata: bool = False):
        return self.__connection__.executemany(fmt, data, iscommit, isdata)
    
    def executequery(self, query, iscommit : bool = False, isdata: bool = False):
        return self.__connection__.executequery(query, iscommit, isdata)

    @property
    def connection(self):
        return self.__connection__