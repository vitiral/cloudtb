from unittest import TestCase
import threading
import multiprocessing


from cloudtb import parallel


class TestThread(TestCase):
    def test_output(self):
        # standard threading module, no output
        std = threading.Thread(target=lambda: 42)
        std.start()
        assert std.join() is None
        # new threading module, output
        t = parallel.Thread(target=lambda: 42)
        t.start()
        assert t.join() == 42

    def test_error(self):
        # standard threading module, no way error handling
        std = threading.Thread(target=lambda: 1 / 0)
        std.start()
        std.join()  # no error
        # new threading module raises error
        t = parallel.Thread(target=lambda: 1 / 0)
        t.start()
        with self.assertRaises(ZeroDivisionError):
            t.join()


class TestProcess(TestCase):
    def test_output(self):
        # standard module, no output
        std = multiprocessing.Process(target=lambda: 42)
        std.start()
        assert std.join() is None
        # new module, output
        p = parallel.Process(target=lambda: 42)
        p.start()
        assert p.join() == 42

    def test_error(self):
        # standard module, no way error handling
        std = multiprocessing.Process(target=lambda: 1 / 0)
        std.start()
        std.join()  # no error
        # new module raises error
        p = parallel.Process(target=lambda: 1 / 0)
        p.start()
        with self.assertRaises(ZeroDivisionError):
            p.join()
