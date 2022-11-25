from .._sock import (
    _sock_object,
    socket
)

from .._dict_common_ import (
    commonport
)

from ...typings import (
    strOrBytes,
    strOrBytesPath
)

from ...supported._thread import ThreadHandling

from ...supported._queue import Queue

from ..TCPServer.tcpserver import TCPServer

from ..func import request, response

from typing import *

import ssl

class httpserver(_sock_object):
    def __init__(
            self, 
            host, 
            port, 
            listen: int = 20):
        self.__tcp_server__ = TCPServer(host, port, listen)
        self.__ca_file__ = None
        self.__key_file__ = None
        self.__context__ = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.__ssl_sock__ = None
        self.__is_https__ = False
    
    def config(
            self, 
            ca_file: strOrBytesPath = None, 
            key_file: strOrBytesPath = None):
        self.__ca_file__ = ca_file
        self.__key_file__ = key_file
        if ca_file and key_file:
            try: 
                self.__context__.load_cert_chain(ca_file, key_file)
                self.__is_https__ = True
            except: raise FileNotFoundError
        else:
            self.__is_https__ = False

    def connect(self):
        self.__tcp_server__.connect()
        if self.__is_https__: self.__ssl_sock__ = self.__context__.wrap_socket(self.__tcp_server__.connection, server_side=True)
        else: self.__ssl_sock__ = self.__tcp_server__.connection

    def disconnect(self):
        self.__tcp_server__.disconnect()
    
    def reconnect(
            self,
            ca_file: strOrBytesPath = None, 
            key_file: strOrBytesPath = None):
        self.__tcp_server__.disconnect()
        self.config(ca_file, key_file)
        self.connect()

    def accept(self):
        return self.__ssl_sock__.accept()
        

def _default_handling(sock, address, *args, **kargs):
    print(f'[+]Connect from {address[0]}:{address[1]}')
    k = request(sock, 1024)
    response(sock, b"""HTTP/1.1 200 OK
Date: Mon, 27 Jul 2009 12:28:53 GMT
Server: Apache/2.2.14 (Win32)
Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
Content-Length: 88
Content-Type: text/html

<html>
<body>
<h1>Hello, World!</h1>
</body>
</html>""")

def _default_end_handling(sock, address, *args, **kargs):
    try: sock.close()
    except: pass

def loop_forever_http_server(
        host: str,
        port : int,
        *args,
        listen: int = 20,
        **kwargs
    ) -> None:
    tmp = httpserver(host, port, listen)
    func_handling = kwargs.pop('handling_func', _default_handling)
    end_handling = kwargs.pop('end_handling', _default_end_handling)
    ca_file = kwargs.pop('ca_file', None)
    key_file = kwargs.pop('key_file', None)
    tmp.config(ca_file, key_file)
    tmp.connect()
    while True: 
        try: ThreadHandling(None, func_handling, end_handling, *(tmp.accept())).start()
        except: break