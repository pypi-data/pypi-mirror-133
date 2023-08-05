import filelock


class LockDirectory(object):
    def __init__(self, directory):
        self.directory = directory
        self.locker = filelock.FileLock(f"{directory}/locker.lock")

    def __enter__(self):
        self.locker.acquire()
        return self

    def __exit__(self, *args):
        self.locker.release()
