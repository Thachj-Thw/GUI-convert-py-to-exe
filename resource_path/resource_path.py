def path():
    import sys
    import os
    try:
        return sys._MEIPASS
    except AttributeError:
        return os.path.abspath(".")
