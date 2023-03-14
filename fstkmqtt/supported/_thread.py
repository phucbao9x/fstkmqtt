try:
    from threading import Thread, Lock, Event
    from ..typings import t
except:
    exit(0)

class ThreadHandling(Thread):
    def __init__(
            self, 
            enter_func: t.Callable[..., object] | None = None,
            func : t.Callable[..., t.Any] | None = None,
            end_func: t.Callable[..., t.Any] | None = None,
            *args, 
            queue = None,
            **kwargs
            ) -> None:
        self.__enter_func__ = enter_func if enter_func and hasattr(enter_func, '__call__') else lambda *a, **b: None
        self.__func__ = func if func and hasattr(func, '__call__') else lambda *a, **b: None
        self.__end_func__ = end_func if end_func and hasattr(end_func, '__call__') else lambda *a, **b: None
        self.__args__ = args
        self.__kwargs__ = kwargs
        self.__eventset__ = Event()
        Thread.__init__(self)
        self.__lock__ = Lock()

    def run(self):
        self.__enter_func__(*self.__args__, **self.__kwargs__)
        self.__func__(*self.__args__, **self.__kwargs__)
        self.__end_func__(*self.__args__, **self.__kwargs__)