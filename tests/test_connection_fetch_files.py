import os
from unittest import mock

from ftptools.connection import Connection

from . import helpers


@mock.patch.object(Connection, 'refresh', new=helpers._refresh)
def test_fetch_files_normal(tmpdir):
    obj = Connection(None, None, None)
    # use pytest tmpdir in place of store
    obj.store.cleanup()
    obj.store.name = tmpdir
    # mock conn member
    obj.conn = helpers._Conn(
        nlst=helpers._nlst, retrbinary=helpers._retrbinary
    )
    # invoke method
    obj.fetch_files()
    assert os.listdir(tmpdir)[0] == 'file1.txt'


@mock.patch.object(Connection, 'refresh', new=helpers._refresh)
def test_fetch_files_returns_fails(tmpdir):
    obj = Connection(None, None, None)
    # use pytest tmpdir in place of store
    obj.store.cleanup()
    obj.store.name = tmpdir
    # mock conn member
    obj.conn = helpers._Conn(
        nlst=helpers._nlst, retrbinary=helpers._raise_os_error
    )
    # invoke method
    results = obj.fetch_files()
    assert results[0] == 'file1.txt'
