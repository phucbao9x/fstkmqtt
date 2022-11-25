def isexists(inside:str, characters : list): return any([inside.count(character) for character in characters])

def kwsets(**kwargs) :
    return kwargs

import typing as _t____

F = _t____.Callable[..., _t____.Any]

from functools import update_wrapper

def setup_method(f):
    _name_ = f.__name__
    def innermethod(self, *args, **kwargs):
        if self._check_function_name_is_not_exists(_name_): 
            return f(self, *args, **kwargs)
    return _t____.cast(F, update_wrapper(innermethod, f))