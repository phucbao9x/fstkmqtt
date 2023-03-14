from ...TCPServer.tcpserver import TCPServer
from ..._sock import (
    _sock_object,
    socket
)

from ....typings import (
    strOrBytes,
    strOrBytesPath
)

from ...func import request, response

from ....supported._thread import ThreadHandling

from ....supported._queue import Queue

from ...TCPServer.tcpserver import TCPServer

from typing import *

import json,random

class mqttserver(_sock_object):
    def __init__(self, host, port, listen: int = 20):
        try:
            self.__tcp_server__ = TCPServer(host, port, listen)
        except:
            print(f"We can't open MQTT server at {host}:{port}")
        self.__address_server__ = (host, port)
        self.__listen__ = listen
        self.__f__ = "C:\\Users\\Admin\\AppData\\Local\\Temp\\tempdata.json"
        self.__fs__ = "C:\\Users\\Admin\\AppData\\Local\\Temp\\subcribe.json"

        def connack(**options):
            data = options['data']
            messengerlen = data[1] & 0xff
            protocollen = (data[2] & 0xffff) << 8 | data[3] & 0xff
            protocolname = data[4:4 + protocollen]
            protocolver = data[4 + protocollen]
            next = 4 + protocollen
            connectflag = data[next + 1]
            protocollen = (data[next + 2] & 0xffff) << 8 | data[next + 3] & 0xff
            clientIDLen = (data[next + 4] & 0xffff) << 8 | data[next + 5] & 0xff
            clientID = data[next+6:next+6 + clientIDLen]
            return b"\x20\x02\x00\x00", clientID

        def pubrel(**options):
            pass

        def whenhaspublish(**options):
            data = options['data']
            qesv = (data[0] & 0b00000110)
            topiclenght = (data[2] & 0xff) << 8 | (data[3] & 0xff)
            topicname = data[4:topiclenght+4]
            value = data[topiclenght+4:]
            file = options['file']

            data = {}
            
            try:
                with open(file) as json_file:
                    data = json.load(json_file)
            except:
                with open(file, 'a') as json_file:
                    pass
            tmp = topicname.decode()
            if tmp not in data:
                data[tmp] = {}
                data[tmp]['value'] = value.decode()
                data[tmp]['id'] = 1
            else:
                data[tmp]['value'] = value.decode()
                data[tmp]['id'] += 1
                if data[tmp]['id'] == 2**8:
                    data[tmp]['id'] = 1
            id = data[tmp]['id']
            id = chr(id).encode()
            if len(id) == 1:
                id = bytes(1) + id
            
            with open(file, 'w') as json_file:
                json_file.truncate(0)
                json_file.write(json.dumps(data))
            

            def puback(**options):
                return b'\x40\02' + options["id"]

            def pubrec(**options):
                pass
            def nothing(**options):
                return
            
            qes = {
                0 : nothing,
                1 : puback,
                2 : pubrec
            }
            return qes[qesv](data=data, file=file, id=id)


        def pubcomp(**options):
            pass

        def wantpublish(**options):
            file = options['file']
            files = options['files']
            clientID = options['clientID']
            data2 = {}
            while not data2:
                try:
                    with open(file) as json_files:
                        data2 = json.load(json_files)
                except: pass
            data1 = {}
            while not data1:
                try:
                    with open(files) as json_file:
                        data1 = json.load(json_file)
                except: pass
            result = list()
            tmpclientID = clientID.decode()
            if tmpclientID not in data1:
                return result
            for topicname in data1[tmpclientID]:
                idjs = data1[tmpclientID][topicname]['id']
                try:
                    idtmp = data2[topicname]['id']
                    if idjs == idtmp: continue
                except: pass
                value = data2[topicname]['value']
                lentopicname = len(topicname)
                lentopicname = chr(lentopicname).encode()
                if len(lentopicname) == 1:
                    re = bytes(1) + lentopicname 
                else: re = lentopicname
                re += topicname.encode() + value.encode()
                re = chr(len(re)).encode() + re
                re = b'\x30' + re

                data1[tmpclientID][topicname]['id'] = idtmp
                
                with open(files, 'w') as json_file:
                    json_file.truncate(0)
                    json_file.write(json.dumps(data1))

                result.append(re)
            return result

        def subscribe(**options):
            data = options['data']
            file = options['file']
            files = options['files']
            clientID = options['clientID']
            cl = options['client']
            func = options['func']
            remaininglenght = (data[1] & 0xff)
            idmessenger = (data[2] & 0xff) << 8 | (data[3] & 0xff)
            topiclenght = (data[4] & 0xff) << 8 | (data[5] & 0xff)
            topicname = data[6:topiclenght+6]
            qos = data[-1]
            idmessenger += 1
            idmessenger = chr(idmessenger).encode()
            subcribeack = b'\x90\x02'
            if len(idmessenger) == 1:
                subcribeack += bytes(1) + idmessenger
                
            data = {}
            
            try:
                with open(files) as json_file:
                    data = json.load(json_file)
            except:
                with open(files, 'a') as json_file:
                    pass
            
            tmpClientID = clientID.decode()
            k = topicname.decode()
            if tmpClientID not in data:
                data[tmpClientID] = {}
                data[tmpClientID][k] = {}
                data[tmpClientID][k]['id'] = 0
            else:
                if k not in data[tmpClientID]:
                    data[tmpClientID][k] = {}
                    data[tmpClientID][k]['id'] = 0
            with open(files, 'w') as json_file:
                json_file.truncate(0)
                json_file.write(json.dumps(data))
            def loopwant(func, f, fs, clientID, cl):
                while True:
                    dt = func(file=f, files = fs, clientID = clientID)
                    if len(dt):
                        for i in dt:
                            response(cl, i)
            j = ThreadHandling(None, loopwant, None, func, file, files, clientID, cl)
            j.start()
            return subcribeack, clientID

        def whenhaspuback(**options):
            pass

        def whenhaspubcomp(**options):
            pass

        def whensuback(**options):
            pass

        def unsubcribe(**options):
            pass

        def unsuback(**options): pass

        def pingreq(**option) : return b"\xd0\x00"

        def pong(**options) : return

        self.__switcher = {
            1 : connack,
            3 : whenhaspublish,
            4 : whenhaspuback,
            5 : pubrel,
            6 : pubcomp,
            7 : whenhaspubcomp,
            8 : subscribe,
            9 : whensuback,
            10: unsubcribe,
            11: unsuback,
            12: pingreq,
            13: pong,
            15: wantpublish
        }
    
    def __handling_messenger__(cl, addr, switcher, f, fs):
        ClientID = None
        RUN = []
        while True:
            def processdata(data, clientID):
                method = (data[0] & 0xf0) >> 4
                qes = (data[0] & 0x0f)
                remaininglenght = 0
                multifi = 1
                location = 1
                while True:
                    digit = data[location]
                    remaininglenght += (digit &  127) * multifi
                    if digit & 128 == 0: break
                    multifi *= 128
                    location += 1
                firstpayload = data[location+1:location+1+remaininglenght]
                secondData = data[1+location+remaininglenght:]
                if method == 14:
                    cl.close()
                    return
                dt = switcher[method](data=data, file=f, payload = firstpayload, files = fs, clientID = clientID, func=switcher[15], client = cl)
                if type(dt) is tuple:
                    dt, clientID = dt
                    response(cl, dt)
                elif type(dt) is list:
                    for i in dt:
                        response(cl, i)
                elif dt: response(cl, dt)
                if len(secondData):
                    processdata(secondData, clientID)
                if method == 12:
                    return
                return clientID
            ClientID = processdata(request(cl), ClientID)
            if ClientID == None: 
                RUN.clear()
                break

    def __handling_end__(cl, addr, switcher, f, fs):
        cl.close()

    def run(self):
        try:
            self.__tcp_server__.connect()
        except:
            print(f"We can't open MQTT server at {':'.join(self.__address_server__)}")
        while True:
            _c, _a = self.__tcp_server__.accept()
            ThreadHandling(
                None, 
                mqttserver.__handling_messenger__, 
                mqttserver.__handling_end__, 
                *(_c, _a, self.__switcher, self.__f__, self.__fs__)).start()
           