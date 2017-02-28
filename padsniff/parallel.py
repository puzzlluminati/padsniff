from copy import deepcopy
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

    Arguments passed to the decorated function are deep-copied to
    allow for thread-safe behavior.
    """
    qualname = getattr(func, '__qualname__', None)

    def run(*args, **kwargs):
        """Wraps execution of %s(*args, **kwargs) in a thread.""" % qualname
        t = cls(
            target=func,
            name=qualname,
            args=deepcopy(args),
            kwargs=deepcopy(kwargs),
        )
        t.start()

    # apply __wrapped__ attr to be consistent with functools.wraps
    run.__wrapped__ = getattr(func, '__wrapped__', func)

    return run
