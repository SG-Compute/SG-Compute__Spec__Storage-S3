# ═══════════════════════════════════════════════════════════════════════════════
# Tests — sg_s3_server backends: test_S3__Backend__Storage_FS
# Memory-FS adapter using in-memory storage. No AWS, no network.
# Skips if memory-fs is not installed.
# ═══════════════════════════════════════════════════════════════════════════════

import unittest
from unittest                                                                       import TestCase


try:
    from sg_s3_server.backends.S3__Backend__Storage_FS                             import S3__Backend__Storage_FS
    HAS_MEMORY_FS = True
except ImportError:
    HAS_MEMORY_FS = False


@unittest.skipUnless(HAS_MEMORY_FS, 'memory-fs not installed')
class test_S3__Backend__Storage_FS(TestCase):

    def setUp(self):
        self.backend = S3__Backend__Storage_FS()
        self.backend.setup(storage_type='memory')

    def test_create_bucket(self):
        self.backend.create_bucket('test-bucket')
        names = [b['Name'] for b in self.backend.list_buckets()]
        assert 'test-bucket' in names

    def test_put_and_get_round_trip(self):
        self.backend.create_bucket('my-bucket')
        self.backend.put('my-bucket', 'hello.txt', b'hello world', {})
        data = self.backend.get('my-bucket', 'hello.txt')
        assert data == b'hello world'

    def test_get_missing_returns_none(self):
        result = self.backend.get('no-bucket', 'no-key')
        assert result is None

    def test_head_returns_metadata(self):
        self.backend.create_bucket('hd')
        self.backend.put('hd', 'file.bin', b'hello', {})
        info = self.backend.head('hd', 'file.bin')
        assert info is not None
        assert info['ContentLength'] == 5

    def test_head_missing_returns_none(self):
        result = self.backend.head('x', 'y')
        assert result is None

    def test_delete_removes_object(self):
        self.backend.create_bucket('del')
        self.backend.put('del', 'gone.txt', b'bye', {})
        self.backend.delete('del', 'gone.txt')
        assert self.backend.get('del', 'gone.txt') is None

    def test_list_objects_in_bucket(self):
        self.backend.create_bucket('ls')
        self.backend.put('ls', 'a.txt', b'aa', {})
        self.backend.put('ls', 'b.txt', b'bb', {})
        objs = self.backend.list('ls')
        keys = [o['Key'] for o in objs]
        assert 'a.txt' in keys
        assert 'b.txt' in keys

    def test_list_with_prefix(self):
        self.backend.create_bucket('pf')
        self.backend.put('pf', 'logs/a.txt', b'a', {})
        self.backend.put('pf', 'data/b.txt', b'b', {})
        objs = self.backend.list('pf', prefix='logs/')
        keys = [o['Key'] for o in objs]
        assert 'logs/a.txt' in keys
        assert 'data/b.txt' not in keys
