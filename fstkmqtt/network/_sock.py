from ._import_ import (
    strOrNope,
    socket,
    strOrBytesPath,
    Any,
    strOrBytes,
    setup_method
)

from ..supported._queue import Queue
from ..supported._thread import ThreadHandling

class _sock_object:
    def __init__(
            self, 
            host, 
            port, 
            listen: int = 20,
            ca_file: strOrBytesPath = None,
            key_flie : strOrBytesPath = None):
        self.__host__ = host
        self.__port__ = port
        self.__listen__ = listen
        self.__ca_file__ = ca_file
        self.__key_file__ = key_flie
        self.__connection__ = None
        self.__dfunc__ = {}
        self.__fname__ = []

    def config(
            self,
            ca_file : strOrBytesPath = None, 
            key_file : strOrBytesPath = None):
        self.__ca_file__ = ca_file
        self.__key_file__ = key_file

    def connect(self):
        raise NotImplementedError
    
    def reconnect(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError
    
    def _add_handling(self, request, funct):
        raise NotImplementedError

    @setup_method
    def add_handling(self, request):
        def decorater(f):
            self._add_handling(request, f)
        return decorater
    
    def _get_request(data):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError

Queue = Queue
ThreadHandling = ThreadHandling