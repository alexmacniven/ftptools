from unittest import mock

import pytest

from ftptools.connection import Connection


class _Conn:
    def __init__(self):
        self.mlsd = None


def _refresh(*args, **kwargs):
    return 0


def _mlsd(*args, **kwargs):
    return [('myfile', {'modify': 123})]


def test_fetch_modtime_basic():
    with mock.patch.object(Connection, 'refresh', new=_refresh):
        obj = Connection(None, None, None)
        obj.conn = _Conn()
        obj.conn.mlsd = _mlsd
        result = obj.fetch_modtime('myfile')
        assert result == 123


def test_fetch_modtime_not_found():
    with mock.patch.object(Connection, 'refresh', new=_refresh):
        obj = Connection(None, None, None)
        obj.conn = _Conn()
        obj.conn.mlsd = _mlsd
        with pytest.raises(FileNotFoundError):
            obj.fetch_modtime('notmyfile')
