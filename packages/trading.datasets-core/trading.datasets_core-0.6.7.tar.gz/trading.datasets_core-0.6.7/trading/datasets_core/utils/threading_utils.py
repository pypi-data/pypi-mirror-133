"""Module containing an extended Thread class."""

from threading import Thread


class PropagatingThread(Thread):
    """Extended Thread that allows propagation of exceptions."""

    def run(self):
        self.exc = None
        try:
            self.ret = self._target(*self._args, **self._kwargs)
        except BaseException as error:
            self.exc = error

    def join(self, timeout=None):
        super().join(timeout)
        if self.exc:
            raise self.exc
        return self.ret
