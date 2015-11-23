''' Better threading and multiprocessing '''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys
import traceback
import threading
import multiprocessing


class Thread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(Thread, self).__init__(*args, **kwargs)
        self.output = None
        self.exc_info = None
        if not hasattr(self, '_target'):  # python2/3 compatibility
            self._target = self._Thread__target
            self._args = self._Thread__args
            self._kwargs = self._Thread__kwargs

    def run(self, *args, **kwargs):
        try:
            self.output = self._target(*self._args, **self._kwargs)
        except Exception:
            self.exc_info = sys.exc_info()

    def join(self, *args, **kwargs):
        super(Thread, self).join(*args, **kwargs)
        if self.exc_info:
            if sys.version_info[0] == 3:
                raise self.exc_info[0]
            else:
                exec('e=self.exc_info; raise e[0], e[1], e[2]')
        return self.output


class Process(multiprocessing.Process):
    def __init__(self, *args, **kwargs):
        super(Process, self).__init__(*args, **kwargs)
        self._channel = multiprocessing.Queue()

    def run(self, *args, **kwargs):
        try:
            self._channel.put(self._target(*self._args, **self._kwargs))
        except Exception as e:
            e.tb_str = traceback.format_exc()
            self._channel.put(e)

    def join(self, *args, **kwargs):
        super(Process, self).join(*args, **kwargs)
        output = self._channel.get()
        if isinstance(output, BaseException):
            raise output
        return output
