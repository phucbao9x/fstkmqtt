def isexists(inside:str, characters : list): return any([inside.count(character) for character in characters])

def kwsets(**kwargs) :
    return kwargs

from .detecttype import istype

import typing as _t____

F = _t____.Callable[..., _t____.Any]

from functools import update_wrapper

def setup_method(f):
    def innermethod(self, *args, **kwargs):
        return f(self, *args, **kwargs)
    return _t____.cast(F, update_wrapper(innermethod, f))

def getinfomation(request):
    requestes = request.splitlines()
    re ={}
    #Line 1:
    tmp_line1 = requestes[0].split()
    re['method'] = tmp_line1[0]
    re['baseurl'] = tmp_line1[1]
    re['version'] = tmp_line1[2]

    del tmp_line1

    for i in requestes[1:]:
        if i:
            tmp_line = i.split(":", 1)
            re[tmp_line[0]] = tmp_line[1]
    return re

def getresponse(dict_response:dict|str) -> bytes:
    if istype(data, str):
        return data.encode()
    else:
        data = ""
        #Line 1:
        version = dict_response.pop('version', 'HTTP/1.1')
        num_code = dict_response.pop('num_code', 200)
        status = dict_response.pop('status', 'OK')
        data += ' '.join([version, num_code, status]) + '\n'

        for i in dict_response:
            data += ' : '.join([i, dict_response[i]]) + '\n'
        return data.encode()