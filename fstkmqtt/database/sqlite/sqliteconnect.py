from sqlite3 import (
    Connection as __Conn__,
    connect as conn)
import os
from ...supported.detecttype import (
    istype,
    anytype
)

from ...typings import (
    t
)
Type = t.Type
List = list

from ...exceptions import (
    MissingDataException
)

from ..connect import connect

class sqliteconnect(connect):
    def __init__(self):
        self.__db__ = None
        self.__timeout__ = None
        self.__detect_types__ = None
        self.__isolation_level__ = None
        self.__check_same_thread__ = None
        self.__factory__ = None
        self.__cached_statements__ = None
        self.__uri__ = None
        self.__conn__ = None
        self.__autocommit__ = False

    def config(
            self, 
            database: str,
            timeout : float = 5.0,
            detect_types: int = 0,
            isolation_level : str | None = 'DEFERRED',
            check_same_thread : bool = True,
            factory : Type[__Conn__]| None = __Conn__,
            cached_statements : int = 128,
            uri : bool = False,
            autocommit: bool = False
            ):
        self.__db__ = database
        self.__timeout__ = timeout
        self.__detect_types__ = detect_types
        self.__isolation_level__ = isolation_level
        self.__check_same_thread__ = check_same_thread
        self.__factory__ = factory
        self.__cached_statements__ = cached_statements
        self.__uri__ = uri
        self.__is_connected__ = False
        self.__autocommit__ = autocommit
        
    def connect(self):
        if self.__is_connected__: return
        try:
            self.__conn__ = __Conn__(
                self.__db__, 
                self.__timeout__, 
                self.__detect_types__,
                self.__isolation_level__,
                self.__check_same_thread__,
                self.__factory__,
                self.__cached_statements__,
                self.__uri__)
            self.__is_connected__= True
            print(f'Connect to {self.__db__}')
        except TypeError as T:
            print(f'Can\'t connect to a missing database.')
        except:
            print(f'Can\'t create a connection to your database.')

    def disconnect(self):
        if not self.__is_connected__: return
        self.__conn__.close()
        self.__is_connected__ = False
    
    def reconnect(self, database: str):
        if self.__is_connected__: 
            self.__conn__.close()
        self.__db__ = database if database else self.__db__
        try:
            self.__conn__ = __Conn__(
                self.__db__, 
                self.__timeout__, 
                self.__detect_types__,
                self.__isolation_level__,
                self.__check_same_thread__,
                self.__factory__,
                self.__cached_statements__,
                self.__uri__)
            self.__is_connected__= True
        except TypeError as T: print(f'Can\'t connect to a missing database.')
        else: print(f'Can\'t create a connection to your database.')

    def execute(self, fmt, data:tuple|None = None, iscommit: bool = False, isdata = False):
        cursor = self.__conn__.cursor()
        cursor.execute(fmt, data)
        if self.__autocommit__ or iscommit: self.__conn__.commit()
        if isdata: return cursor.fetchall()

    def executemany(self, fmt, data:list[tuple]|None = None, iscommit: bool = False, isdata = False):
        cursor = self.__conn__.cursor()
        cursor.executemany(fmt, data)
        if self.__autocommit__ or iscommit: self.__conn__.commit()
        if isdata: return cursor.fetchall()

    def executequery(self, query, iscommit: bool = False, isdata = False):
        cursor = self.__conn__.cursor()
        cursor.execute(query)
        if self.__autocommit__ or iscommit: self.__conn__.commit()
        if isdata: return cursor.fetchall()

    def insert(self, tablename : str| type, **kwdata):
        fmt = 'INSERT INTO %s (%s) VALUES (%s);'
        qr = fmt%(tablename, ', '.join(list(kwdata)), ', '.join([str(i) if not istype(i, str) else f'\'{i}\'' for i in list(kwdata.values())]))
        cursor = self.__conn__.cursor()
        cursor.execute(qr)
        self.__conn__.commit()
        
    def insertmany(self, tablename : str| type, data : list[dict]):
        for i in data:
            self.insert(tablename, i)

    def select(self, tablename, condition : str|None = None,*columns: type|str):
        fmt = 'SELECT %s FROM %s%s;'
        cols = '*' if not columns else ', '.join([col().__name__ if istype(col, type) else col for col in columns])
        condition = (' WHERE ' if condition else '') + condition
        qr = fmt%(cols, tablename, condition)
        cursor = self.__conn__.cursor()
        cursor.execute(qr)
        return cursor.fetchall()
    
    def selectmany(self, tablename: str, columns: tuple, *conditions):
        res = []
        for condition in conditions:
            res.append(self.select(tablename, condition, *columns))
        return res
    
    def update(self, tablename, condition: str, **column_data_pair: list[tuple]|tuple):
        if istype(tablename, type): tablename = tablename().__name__
        fmt = 'UPDATE %s SET %s WHERE %s;'
        if not condition or not column_data_pair: raise MissingDataException('Can\'t be update your data when missing \'condition\' or column_data_pair that needed to be refresh')
        set_ = ', '.join([f'{i}={column_data_pair[i]}' for i in column_data_pair])
        self.execute(fmt, (tablename, set_, condition), True)
    
    def updatemany(self, tablename, *conditions, **column_data_pair):
        for condition in conditions:
            self.update(tablename, condition, **column_data_pair)

    def delete(self, tablename, wherefmt: str, datawhere: tuple):
        fmt = f'DELETE FROM {tablename} WHERE %s'
        self.execute(fmt%wherefmt, datawhere, True)

    def deletemany(self, tablename, wherefmt: str, *datawherestore: tuple):
        fmt = f'DELETE FROM {tablename} WHERE %s'
        for datawhere in datawherestore: self.execute(fmt%wherefmt, datawhere, True)

MissingDataException = MissingDataException