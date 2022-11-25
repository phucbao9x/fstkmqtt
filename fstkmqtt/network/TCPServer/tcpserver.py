from .._sock import (
    _sock_object,
    socket
)

from .._dict_common_ import (
    commonport
)

from ...supported._thread import ThreadHandling

from ...supported._queue import Queue

from typing import *

class TCPServer(_sock_object):
    def __init__(
            self, 
            host = 'localhost', 
            port = commonport['apptcp'], 
            listen: int = 20):
        self.__host__ = socket.gethostbyname(host)
        self.__port__ = port if 1<= port <= 2**16 - 1 else commonport['apptcp']
        self.__listen__ = listen

        self.__connection__ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__isconnected__ = False

    def _check_function_name_is_not_exists(self, fname):
        raise NotImplementedError

    def config(self, host, port):
        self.__host__ = socket.gethostbyname(host) if host else self.__host__
        self.__port__ = port if 1 <= port <= 2**16 - 1 else self.__port__
    
    def connect(self):
        try:
            self.__connection__.bind((self.__host__, self.__port__))
            self.__connection__.listen(self.__listen__)
            self.__isconnected__ = True
        except OSError:
            print(f'Can\'t open port {self.__port__} for {self.__host__} server. Because it opened in the another app.')
    
    def disconnect(self):
        if self.__isconnected__: self.__connection__.close()

    def reconnect(self):
        if not self.__isconnected__: self.__connection__.bind((self.__host__, self.__port__))
    
    def accept(self):
        return self.__connection__.accept()

    @property
    def connection(self):
        return self.__connection__

def _default_handling(sock, address, *args, **kargs):
    print(address)

def _default_end_handling(sock, address, *args, **kargs):
    sock.close()

def loop_forever_tcp_server(
        host: str,
        port : int,
        *args,
        listen: int = 20,
        **kwargs
    ) -> None:
    tmp = TCPServer(host, port, listen)
    __queue__ = Queue()
    tmp.connect()
    func_handling = kwargs.pop('handling_func', _default_handling)
    end_handling = kwargs.pop('end_handling', _default_end_handling)
    while True: 
        try: ThreadHandling(None, func_handling, end_handling, *(tmp.accept()), queue=__queue__).start()
        except: pass