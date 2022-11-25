from typing import Any

class Queue:
    def __init__(self):
        self.__data__ = []

    def add(self, value: Any):
        self.__data__.append(value)
    
    def lastitem(self):
        try: return self.__data__[-1]
        except IndexError as i: print(i)
    
    def item(self, index):
        try: return self.__data__[index]
        except IndexError as i:print(i)

    def popitem(self, index):
        try: return self.__data__.pop[index]
        except IndexError as i: print(i)
    
    def changeitem(self, index, value):
        try: self.__data__[index] = value
        except IndexError as i: print(i)

    def remove(self, value):
        try: self.__data__.remove(value)
        except ValueError as v: print(v)