class _Conn:
    def __init__(self, mlsd=None, nlst=None, retrbinary=None):
        self.mlsd = mlsd
        self.nlst = nlst
        self.retrbinary = retrbinary


def _refresh(*args, **kwargs):
    return 0


def _nlst(*args, **kwargs):
    return ['file1.txt']


def _retrbinary(*args, **kwargs):
    return 0


def _raise_os_error(*args, **kwargs):
    raise OSError
