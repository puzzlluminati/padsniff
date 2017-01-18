from weakref import WeakSet
from netlib.basethread import BaseThread


class HandlerThread(BaseThread):

    instances = WeakSet()


    def __new__(cls, *args, **kwargs):
        inst = super().__new__(cls, *args, **kwargs)
        cls.instances.add(inst)
        return inst


def threaded(func):

    def run(*args, **kwargs):
        t = HandlerThread(
            func.__qualname__,
            target=func,
            args=args,
            kwargs=kwargs,
        )
        t.start()

    return run