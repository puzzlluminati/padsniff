from threading import Thread
from weakref import WeakSet


class HandlerThread(Thread):
    """Thread subclass that keeps track of its instances."""

    instances = WeakSet()

    def __new__(cls, *args, **kwargs):
        inst = super().__new__(cls)
        cls.instances.add(inst)
        return inst


def parallelize(func, *, cls=HandlerThread):
    """
    Decorator to run `func` in parallel with the main thread/process.

    `cls` can be any callable that implements a threading.Thread-like
    signature and a start method, including multiprocessing.Process.
    """

    def run(*args, **kwargs):
        t = cls(
            target=func,
            name=getattr(func, '__qualname__', None),
            args=args,
            kwargs=kwargs
        )
        t.start()

    return run