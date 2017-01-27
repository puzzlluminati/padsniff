from threading import enumerate as all_threads, main_thread, Event, Thread
from time import sleep

from padsniff.parallel import parallelize, HandlerThread

from pytest import fixture


@fixture(autouse=True)
def join_threads():
    # can't join main thread because it's running our tests
    threads = set(all_threads()) - {main_thread()}
    for thread in threads:
        thread.join()


class TestHandlerThread:


    def test_instance_tracking(self):
        assert len(HandlerThread.instances) == 0

        handler_thread1 = HandlerThread()
        handler_thread2 = HandlerThread()
        regular_thread = Thread()

        assert len(HandlerThread.instances) == 2
        assert handler_thread1 in HandlerThread.instances
        assert handler_thread2 in HandlerThread.instances
        assert regular_thread not in HandlerThread.instances

        del handler_thread2

        assert len(HandlerThread.instances) == 1


def test_parallelize_nonblocking():
    assert len(all_threads()) == 1
    event = Event()

    def wait_until_event():
        event.wait()

    parallelize(wait_until_event)()

    assert len(all_threads()) == 2

    event.set()
    # give the thread time to wake up
    sleep(0.1)

    assert len(all_threads()) == 1


def test_parallellize_with_args(mocker):
    mock = mocker.Mock()
    name = mock.__qualname__ = 'mock'
    args = 'can dank memes', 'melt steel beams?'
    kwargs = dict(tests='pls pass')
    parallel_func = parallelize(mock)

    parallel_func(*args, **kwargs)

    assert mock.called_once_with(
        target=mock,
        name=name,
        args=args,
        kwargs=kwargs,
    )
    assert mock.start.called_once_with()