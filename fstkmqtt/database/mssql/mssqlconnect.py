# Exported the outsource libraries.
import pymssql as MSSQL

from pymssql import (
    StandardError,
    Warning,
    Error,
    InterfaceError,
    DatabaseError,
    OperationalError,
    IntegrityError,
    InternalError,
    ProgrammingError,
    NotSupportedError,
    ColumnsWithoutNamesError
)

from pymssql import (
    Connection as _Connt_,
    connect as conn,
    _mssql
)

from ...typings import *

from ...exceptions import (
    NullConnectionError,
    MissingDataException
)

from ...supported.detecttype import (
    istype
)

class DATABASECHARSET:
    utf_8 = 'UTF-8'
    utf_16 = 'UTF-16'
    utf_32 = 'UTF-32'
    ascii = 'ASCII'

class SQLServer:
    def __init__(self) -> None:
        self.__server__ : t.Optional[str] = None
        self.__user__ : t.Optional[str] = None
        self.__password__ : t.Optional[str] = None
        self.__databased__ : t.Optional[str] = None
        self.__timeout__ : int = 0
        self.__login_timeout__ : int = 60
        self.__charset__ : str = DATABASECHARSET.utf_8
        self.__as_dict__ : bool = False
        self.__host__ : str = ''
        self.__appname__ : t.Optional[str] = None
        self.__port__ : str  = '1433'
        self.__conn_properties__ = None
        self.__autocommit__ : bool= False
        self.__tds_version__ : t.Optional[str] = None

        self.__connect__ = None
        self.__cursor__ = None
        self.__is_connected__ = False

    def config(
            self,
            user : str,
            password : str,
            databased : str,
            server : str = '.',
            timeout : int = 0,
            login_timeout : int = 60,
            charset : str = DATABASECHARSET.utf_8,
            as_dict : bool = False,
            host : str = '',
            appname : t.Optional[str] = None,
            port : str  = '1433',
            conn_properties = None,
            autocommit : bool= False,
            tds_version : t.Optional[str] = None):
        
        self.__server__ = server 
        self.__user__ = user 
        self.__password__ = password 
        self.__databased__ = databased 
        self.__timeout__ = timeout
        self.__login_timeout__ = login_timeout
        self.__charset__ = charset
        self.__as_dict__ = as_dict
        self.__host__ = host
        self.__appname__ = appname 
        self.__port__ = port
        self.__conn_properties__ = conn_properties
        self.__autocommit__ = autocommit
        self.__tds_version__ = tds_version 
        

    def connect(self):
        if self.__is_connected__: return
        self.__connect__ = conn(
            self.__server__,
            self.__user__,
            self.__password__,
            self.__databased__,
            self.__timeout__,
            self.__login_timeout__,
            self.__charset__,
            self.__as_dict__,
            self.__appname__,
            self.__port__,
            self.__conn_properties__,
            self.__autocommit__,
            self.__tds_version__
        )
        self.__is_connected__ = True
        self.__cursor__ = self.__connect__.cursor()
    
    def execute(self, formatquery: str, data: t.Optional[tuple] = None, iscommit : bool = False):
        if not self.__is_connected__: NullConnectionError
        self.__cursor__.execute(formatquery%(data))
        if self.__autocommit__ or iscommit: self.__connect__.commit()
        if formatquery[:6] == 'SELECT': return self.__cursor__.fetchall()
        return 1
        
    def executemany(self, formatquery: str, data: t.Optional[list[tuple]] = None, iscommit : bool = False):
        if not self.__is_connected__: NullConnectionError
        self.__cursor__.executemany(formatquery%(data))
        if self.__autocommit__ or iscommit: self.__connect__.commit()
        if formatquery[:6] == 'SELECT': return self.__cursor__.fetchall()
        return 1
    
    def select(self, formatstrtabletoend: str, data: t.Optional[tuple] = None, *columns):
        if not self.__is_connected__: raise NullConnectionError
        if not data: raise MissingDataException
        fmt_query = 'SELECT %s ' + formatstrtabletoend%data
        cols = '*' if not columns else ', '.join([column().__name__ if istype(column, type) else column for column in columns])
        self.__cursor__.execute(fmt_query%(cols))
        return self.__cursor__.fetchall()
    
    def selectmany(self, formatstrtabletoend: str, datastore: t.Optional[list[tuple]] = None, *columns):
        if not self.__is_connected__: raise NullConnectionError
        if not datastore: raise MissingDataException
        res = []
        for data in datastore:
            res.append(self.select(formatstrtabletoend, data, *columns))
        return res

    def insert(self, tablename: str, **col_data_pair):
        if not self.__is_connected__: raise NullConnectionError
        if not tablename or not col_data_pair: raise MissingDataException
        fmt_query = 'INSERT INTO %s (%s) VALUES %s'
        cols = ', '.join(list(col_data_pair))
        datas = ', '.join([f'\'{data}\'' if istype(data, str) else str(data) for data in list(col_data_pair.values())])
        self.__cursor__.execute(fmt_query%(tablename,cols, datas))
        self.__connect__.commit()
    
    def insertmany(self, tablename, datastore: t.Optional[list[tuple]] = None):
        for data in datastore:
            self.insert(tablename, data)
    
    def disconnect(self):
        if self.__is_connected__:
            self.__is_connected__ = False
            self.__cursor__.close()
            self.__connect__.close()
    
    def reconnect(
            self,
            user : t.Optional[str] = None,
            password : t.Optional[str] = None,
            databased : t.Optional[str] = None,
            server : t.Optional[str] = None,
            timeout : t.Optional[int] = None,
            login_timeout : t.Optional[int] = None,
            charset : t.Optional[str] = None,
            as_dict : t.Optional[bool] = None,
            host : t.Optional[str] = None,
            appname : t.Optional[str] = None,
            port : t.Optional[str] = None,
            conn_properties = None,
            autocommit : t.Optional[bool]= None,
            tds_version : t.Optional[str] = None
        ):
        if self.__is_connected__:
            self.__cursor__.close()
            self.__connect__.close()
        self.__user__ = user if user else self.__user__
        self.__password__ = password if password else self.__password__
        self.__databased__ = databased if databased else self.__databased__
        self.__server__ = server if server else self.__server__
        self.__timeout__ = timeout if timeout else self.__timeout__
        self.__login_timeout__ = login_timeout if login_timeout else self.__login_timeout__
        self.__charset__ = charset if charset else self.__charset__
        self.__as_dict__ = as_dict if as_dict else self.__as_dict__
        self.__host__ = host if host else self.__host__
        self.__appname__ = appname if appname else self.__appname__
        self.__port__ = port if port else self.__port__
        self.__conn_properties__ = conn_properties if conn_properties else self.__conn_properties__
        self.__autocommit__ = autocommit if autocommit else self.__autocommit__
        self.__tds_version__ = tds_version if tds_version else self.__tds_version__
        self.connect()

NullConnectionError = NullConnectionError
MissingDataException = MissingDataException
MSSQLConnection = _Connt_