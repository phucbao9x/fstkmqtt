# Subject: College project

# Date: 6/11/2022

# Author: Nguyen Tran Phuc Bao

# MySQL remake

#Programming language: Python3

#BEGIN

# Included libraries:
from threading import Thread as T
import random as R
from string import (
    ascii_letters as al,
    digits   as d
)

from socket import gethostbyname

from mysql.connector import (
    connection as Connt,
    MySQLConnection as MYSQLConnt,
    pooling as pl
)

from mysql.connector.pooling import(
    PooledMySQLConnection as pooledConn,
    PoolError as PoolErr
)
from ...typings import (
    t,
    strOrBytesPath
)

from ...exceptions import(
    MissingDataException,
    NotEnoughPrivilege
)

from ...supported.func import (
    isexists,
    kwsets
)
# Declared variables:
DEFAULTLENGHT_SEASION = 120

def createFailoverserver(
        host: str, 
        port: int, 
        user: t.Any, 
        password : t.Any):
    return {
        'host': host,
        'port': port,
        'user' : user,
        'password' : password
    }

from threading import Thread

def configssl(
        tls_versions : t.Optional[str] = None,
        ssl_ca : t.Optional[str] = None,
        ssl_cert: t.Optional[str] = None,
        ssl_key: t.Optional[str] = None,
        key : t.Optional[str] = None,
        tls_ciphersuites : t.Optional[str] = None
        ):
        return {
            'tls_versions' : tls_versions,
            'ssl_ca' : ssl_ca,
            'ssl_cert' : ssl_cert,
            'ssl_key' : ssl_key,
            'key' : key,
            'tls_ciphersuites' : tls_ciphersuites
        }

def configconnectionMySql(
        user : t.Any,
        password: t.Any,
        database : t.Any,
        unix_socket : strOrBytesPath,
        conn_attrs : dict,
        init_commands : t.Any,
        auth_plugin : t.Any,
        fido_callback : t.Callable[...,t.Any],
        time_zone : t.Any,
        sql_mode : t.Any,
        password1 : t.Any = None,
        password2 : t.Any = None,
        password3 : t.Any = None,
        host : str = '127.0.0.1',
        port: int = 3306,
        use_unicode : bool = True,
        charset : t.Any = 'utf8mb4',
        collation: t.Any = 'utf8mb4_general_ci',
        autocommit : bool = False,
        get_warnings: bool = False,
        raise_on_warnings: bool = False,
        connection_timeout : t.Any = None,
        client_flags : t.Any = 0,
        buffered : bool = False,
        raw : bool = False,
        consume_results : bool= False,
        ssl: dict = {},
        ssl_verify_cert: bool = False,
        ssl_verify_identity: bool = False,
        force_ipv6: bool = False,
        oci_config_file : str = '',
        pool_name: t.Any = None,
        pool_size : int = 5,
        pool_reset_session : bool = True,
        compress : bool = False,
        converter_class: t.Optional[type|str] = None,
        converter_str_fallback : bool = False,
        failover : list = [],
        option_files : t.Optional[str] = None,
        option_groups : t.Optional[str] = None,
        allow_local_infile : bool = True,
        use_pure : bool = False,
        krb_service_principal : t.Any = None
    ) -> dict:
    tmp_locals = locals()
    res = {}
    for i in dict(tmp_locals):
        if locals()[i]: res[i] = locals()[i]
    return res

class MySequel:

    # Initialize bulti-function
    def __init__(self) -> None:
        self.__user__  = None
        self.__password__ = None
        self.__database__  = None
        self.__unix_socket__ : str = ""
        self.__conn_attrs__ : dict = {}
        self.__init_commands__  = None
        self.__auth_plugin__ = None
        self.__fido_callback__ = None
        self.__time_zone__  = None
        self.__sql_mode__  = None
        self.__password1__  = None
        self.__password2__  = None
        self.__password3__  = None
        self.__host__ : str = '127.0.0.1'
        self.__port__ : int = 3306
        self.__use_unicode__  = True
        self.__charset__  = 'utf8mb4'
        self.__collation__ = 'utf8mb4_general_ci'
        self.__autocommit__  = False
        self.__get_warnings__ = False
        self.__raise_on_warnings__ = False
        self.__connection_timeout__  = None
        self.__client_flags__  = 0
        self.__buffered__  = False
        self.__raw__  = False
        self.__consume_results__ = False
        self.__ssl__: dict = None
        self.__ssl_verify_cert__ = False
        self.__ssl_verify_identity__ = False
        self.__force_ipv6__ = False
        self.__oci_config_file__ : str = ''
        self.__pool_name__ = None
        self.__pool_size__ = None
        self.__pool_reset_session__ = None
        self.__compress__  = False
        self.__converter_class__ = None
        self.__converter_str_fallback__  = False
        self.__failover__ : list = None
        self.__option_files__ = None
        self.__option_groups__ = None
        self.__allow_local_infile__ = True
        self.__use_pure__ = False
        self.__krb_service_principal__ = None

        self.__config__ = {}

        self.__poolconnection__ = None
        self.__poolList__ = []
        self.__index__ = 0

        self.__cursor__ = None
        self.__connection__ = None

    #All of properties:
    @property
    def username(self): return self.__user__
    @username.setter
    def username(self, value): self.__user__ = value

    @property
    def password(self): return self.__password__
    @password.setter
    def password(self, value): self.__password__ = value

    @property
    def host(self): return self.__host__
    @host.setter
    def host(self, value : str): self.__host__ = gethostbyname(value)

    @property
    def port(self): return self.__port__
    @port.setter
    def port(self, value : int): self.__port__ = value if 1 <= value < 65536 else self.__port__

    @property
    def poolname(self): return self.__pool_name__
    @poolname.setter
    def poolname(self, name: str): self.__pool_name__ = name

    @property
    def poolsize(self): return self.__pool_size__
    @poolsize.setter
    def poolsize(self, size: int): self.__pool_size__ = size

    @property
    def autocommit(self) : return self.__autocommit__
    @autocommit.setter
    def autocommit(self, yesOrNo: bool): self.__autocommit__ = yesOrNo
    
    @property
    def index(self): return self.__index__
    @index.setter
    def index(self, idx:int): self.__index__ = idx

    # Get item bulti-function
    def __getitem__(self, inx):
        if inx < self.__pool_size__:
            return self.__poolList__[inx]
        else: raise IndexError

    # Functions:
    def config(self, **options):
        for i in options:
            self.__dict__[f'__{i}__'] = options[i]

    # For common connection
    def insert(self, tablename, data: t.Optional[dict] = None, **kwdata):
        formatquery = 'INSERT INTO %s (%s) VALUES (%s);'
        cols = ', '.join([*list(data), *list(kwdata)])
        vals = ', '.join([f'\'{i}\'' if type(i) is str else i for i in [*list(data.values()), *list(kwdata.values())]])
        self.__connection__.cursor().execute(formatquery%(tablename, cols, vals))
        if self.__autocommit__ is False:
            self.__connection__.commit()

    def insertmany(self, tablename, datastore : t.Optional[list[dict]] = None):
        for data in datastore:
            self.insert(tablename, data)

    def select(self, data:tuple):
        formatquery = 'SELECT %s FROM %s %s;' 
        self.__connection__.cursor().execute(formatquery%(data))
        return self.__connection__.cursor().fetchall()

    def selectmany(self,datastore: list[tuple]):
        for data in datastore:
            yield self.select(data)

    def update(self, data: tuple):
        formatquery = 'UPDATE %s SETS (%s) WHERE %s;'
        self.__connection__.cursor().execute(formatquery%(data))
        if self.__autocommit__ is False:
            self.__connection__.commit()
    
    def execute(self, formatquery: str, data: t.Optional[tuple] = None, iscommit = True):
        if data: query = formatquery%(data)
        else: query = formatquery
        self.__cursor__.execute(query)
        if self.__autocommit__ is False and iscommit:
            self.__connection__.commit()
        else: return self.__cursor__.fetchall()
    
    def executemany(self, formatquery: str, datastore: t.Optional[list[tuple]] = None, iscommit = True):
        return [self.execute(formatquery, data) for data in datastore]

    def updatemany(self, datastore : list[tuple]):
        for data in datastore:
            self.update(data)
    
    def connect(self, **config):
        print(1)
        if config: self.config(**config)
        tmp = list(self.__dict__.keys())
        config = {}
        for i in range(44):
            if self.__dict__[tmp[i]]:
                config[tmp[i][2:-2]] = self.__dict__[tmp[i]]
        try:
            self.__connection__ = Connt.MySQLConnection(**config)
            self.__cursor__ = self.__connection__.cursor()
            print(f'Connect to db:{self.__database__}//{self.__host__}:{self.__port__} success!')
        except:
            print(f'Can\'t connect to your MySQL server at db:{self.__database__}//{self.__host__}:{self.__port__}')

    def disconnect(self):
        if self.__connection__.is_connected():
            self.__cursor__.close()
            self.__connection__.shutdown()

    def reconnect(self):
        try:
            self.__connection__.connect()
            self.__cursor__ = self.__connection__.cursor()
        except:
            print(f'Can\'t reconnect to your MySQL server at db:{self.__database__}//{self.__host__}:{self.__port__}')

    # For pooled connection
    def poolConnect(self, poolname: str, poolsize: int = 10, is_reset_seasion : bool= False, **kwargs):
        self.config(**kwargs)
        self.__pool_name__ = poolname if poolname else f'PoolConnection<0x{id(self)}>'
        self.__pool_size__ = poolsize
        self.__pool_reset_session__ = is_reset_seasion
        self.__poolList__ = [None] * poolsize
        print(self.__poolList__)
        
        tmp = list(self.__dict__)[:44]
        config = {}
        for i in tmp:
            if self.__dict__[i]:
                config[i[2:-2]] = self.__dict__[i]
        self.__poolconnection__ = pl.MySQLConnectionPool(**config)
        self.__index__ = 0
        while self.__index__ < self.__pool_size__:
            self.__poolList__[self.__index__] = self.__poolconnection__.get_connection()
            self.__index__ += 1
        self.__index__ = 0
    
    def poolDisconnect(self):
        for i in self.__poolList__:
            if i.is_connected():
                i.cursor().close()
                i.close()
        self.__index__ = 0

    def poolReconnect(self):
        for i in range(self.__pool_size__):
            if self.__poolList__[i] is None:
                self.__poolconnection__.add_connection()
                self.__poolList__[i] = self.__poolconnection__.get_connection()
        self.__index__ = 0

    def poolInsert(self, tablename : str, columns : t.Optional[tuple] = None, data : t.Optional[tuple] = None):
        fmtstr = 'INSERT INTO %s %sVALUES (%s)'
        if columns:
            cols = ','.join([c().__name__ if type(c) is type else c for c in columns])
            cols = f'({cols}) '
        else: cols = ''
        if data:
            data = ', '.join([str(i) if type(i) is not str else f'\'{i}\'' for i in data]) 
        if self.__index__ >= self.__pool_size__: self.__index__ = 0
        self.__poolList__[self.__index__].cursor().execute(fmtstr%(tablename, cols, data))
        if self.__autocommit__ is False:
            self.__poolList__[self.__index__].commit()
        self.__index__ += 1
        
    def poolInsertmany(self, tablename : str, columns : t.Optional[tuple] = None, datastore : t.Optional[list[tuple]] = None):
        for data in datastore:
            self.poolInsert(tablename, columns, data)

    def poolDelete(self, tablename: str, condition: t.Optional[str] = None):
        fmtquery = 'DELETE FROM %s WHERE %s;'
        if condition:
            if self.__index__ >= self.__pool_size__: self.__index__ = 0
            self.__poolList__[self.__index__].cursor().execute(fmtquery%(tablename, condition))
            self.__index__ += 1
        else:
            raise MissingDataException
    
    def poolDeletemany(self, tablename: str, conditions: t.Optional[list[str]] = None):
        if conditions:
            for condition in conditions:
                self.poolDelete(tablename, condition)
        else:
            raise MissingDataException

    def poolUpdate(self, tablename: str, **kwsettings):
        '''
parameter "kwsettings" it has constructed:
set = {
    'col1' = 'value1',
    'col2' = 'value2',
},
where = ''
        '''
        fmtquery = 'UPDATE %s SET (%s) WHERE %s'
        if 'where' not in kwsettings:
            raise MissingDataException('Missing where feild')
        if 'set' not in kwsettings:
            raise MissingDataException('Missing set feild')
        if not tablename:
            raise MissingDataException('Missing table name feild')
        where_ = kwsettings['where']
        set_ = kwsettings['set']
        tmpset = []
        for set in set_:
            tmpset.append(f'{set}={set_[set] if type(set_[set]) is not str else f"{set_[set]}"}')
        if self.__index__ >= self.__pool_size__: self.__index__ = 0
        self.__poolList__[self.__index__].cursor().execute(fmtquery%(tablename, ','.join(tmpset), where_))
        if self.__autocommit__ is False:
            self.__poolList__[self.__index__].cursor().commit()
        self.__index__ += 1

    def poolUpdatemany(self, tablename: str, settings: t.Optional[list[dict]] = None):
        for setting in settings:
            self.poolUpdate(tablename, setting)
    
    def poolSelect(self, tablename: str, condition: str,*columns):
        fmt = 'SELECT %s FROM %s%s;'
        if condition: condition = ' WHERE %s'%condition
        cols = ",".join([i().__name__ if type(i) is type else str(i) for i in columns]) if len(columns) else "*"
        if self.__index__ >= self.__pool_size__: self.__index__ = 0
        self.__poolList__[self.__index__].cursor().execute(fmt%(tablename, cols, condition))
        return self.__poolList__[self.__index__].cursor().fetchall()

    def poolSelectmany(self, tablename: str, **settings):
        res = []
        for setting in settings:
            res.append(self.poolSelect(tablename, **setting))
        return res

    def poolExecute(self, formatquery: str, data: t.Optional[tuple] = None, iscommit = False):
        if not data: raise MissingDataException('Missing data argument')
        if not formatquery: raise MissingDataException('Missing formatquery argument')
        if self.__index__ >= self.__pool_size__: self.__index__ = 0
        self.__poolList__[self.__index__].cursor().execute(formatquery%(data))
        if self.__autocommit__ is False and iscommit:
            self.__poolList__[self.__index__].cursor().commit()
            return 1
        else: return self.__poolList__[self.__index__].cursor().fetchall()

    def poolExecutemany(self, formatquery: str, datastore: t.Optional[list[tuple]] = None, iscommit = False):
        if not datastore: raise MissingDataException('Missing data argument')
        if not formatquery: raise MissingDataException('Missing formatquery argument')
        res = []
        for data in datastore:
            res.append(self.poolExecute(formatquery, data, iscommit))
        return res

kwsets = kwsets
isexists = isexists