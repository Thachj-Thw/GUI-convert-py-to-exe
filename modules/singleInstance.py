import os
import sys

from win32event import CreateMutex
from win32api import CloseHandle, GetLastError
from winerror import ERROR_ALREADY_EXISTS


class GetMutex:
    """ Limits application to single instance """
    def __init__(self):
        this_file = os.path.split(sys.argv[0])[-1]
        self.name = this_file + "_{D0E858DF-985E-4907-B7FB-8D732C3FC3B9}"
        self.mutex = CreateMutex(None, False, self.name)
        self.error = GetLastError()

    def is_running(self):
        return self.error == ERROR_ALREADY_EXISTS

    def __del__(self):
        if self.mutex:
            CloseHandle(self.mutex)
