from ..supported.detecttype import istype
from ..exceptions import DangerousRequestException
import re
class SQL:
    def injectionFromQuery(data, fmtdata = None):
        tmp = type(data)
        data = data.decode() if istype(data, bytes) else str(data)
        k = re.finditer("[']*([a-zA-Z0-9_]*)[']*\s*=\s*'([a-zA-Z0-9_]*)'", data)
        m = re.finditer("[']*([a-zA-Z0-9_]*)[']*\s*=\s*'([a-zA-Z0-9_%]*)'", fmtdata)
        lenm = lenk = 0
        for i in k: lenk+=1
        for i in m: lenm+=1
        if lenk != lenm: 
            raise DangerousRequestException('\x1b[38;2;%d;%d;%dmSQL Injection\x1b[0m'%(255, 0, 0))
        return tmp(data)