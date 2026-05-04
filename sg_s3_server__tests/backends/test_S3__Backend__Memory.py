# ═══════════════════════════════════════════════════════════════════════════════
# Tests — sg_s3_server backends: test_S3__Backend__Memory
# In-memory backend. No AWS, no network.
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                       import TestCase

from sg_s3_server.backends.S3__Backend__Memory                                     import S3__Backend__Memory


class test_S3__Backend__Memory(TestCase):

    def setUp(self):
        self.backend = S3__Backend__Memory()
        self.backend.setup()

    def test_create_bucket(self):
        self.backend.create_bucket('my-bucket')
        buckets = self.backend.list_buckets()
        names   = [b['Name'] for b in buckets]
        assert 'my-bucket' in names

    def test_put_and_get_round_trip(self):
        self.backend.create_bucket('b1')
        self.backend.put('b1', 'hello.txt', b'hello world', {})
        data = self.backend.get('b1', 'hello.txt')
        assert data == b'hello world'

    def test_get_missing_returns_none(self):
        result = self.backend.get('no-such-bucket', 'no-such-key')
        assert result is None

    def test_head_returns_metadata(self):
        self.backend.create_bucket('b2')
        self.backend.put('b2', 'file.bin', b'abc', {'Content-Type': 'application/octet-stream'})
        info = self.backend.head('b2', 'file.bin')
        assert info is not None
        assert info['ContentLength'] == 3
        assert 'ETag' in info

    def test_head_missing_returns_none(self):
        result = self.backend.head('x', 'y')
        assert result is None

    def test_delete_removes_object(self):
        self.backend.create_bucket('b3')
        self.backend.put('b3', 'del.txt', b'bye', {})
        self.backend.delete('b3', 'del.txt')
        assert self.backend.get('b3', 'del.txt') is None

    def test_list_objects_in_bucket(self):
        self.backend.create_bucket('b4')
        self.backend.put('b4', 'a.txt', b'aaa', {})
        self.backend.put('b4', 'b.txt', b'bbb', {})
        objs = self.backend.list('b4')
        keys = [o['Key'] for o in objs]
        assert 'a.txt' in keys
        assert 'b.txt' in keys

    def test_list_with_prefix_filter(self):
        self.backend.create_bucket('b5')
        self.backend.put('b5', 'logs/a.txt', b'a', {})
        self.backend.put('b5', 'logs/b.txt', b'b', {})
        self.backend.put('b5', 'data/c.txt', b'c', {})
        objs = self.backend.list('b5', prefix='logs/')
        keys = [o['Key'] for o in objs]
        assert 'logs/a.txt' in keys
        assert 'logs/b.txt' in keys
        assert 'data/c.txt' not in keys

    def test_list_max_keys(self):
        self.backend.create_bucket('b6')
        for i in range(10):
            self.backend.put('b6', f'file{i}.txt', b'x', {})
        objs = self.backend.list('b6', max_keys=3)
        assert len(objs) == 3

    def test_put_creates_bucket_implicitly(self):
        self.backend.put('auto-bucket', 'key.txt', b'data', {})
        assert self.backend.get('auto-bucket', 'key.txt') == b'data'

    def test_list_buckets_empty_initially(self):
        backend2 = S3__Backend__Memory()
        backend2.setup()
        assert backend2.list_buckets() == []

    def test_etag_is_md5_of_content(self):
        import hashlib
        body = b'test-content'
        self.backend.create_bucket('etag-bucket')
        self.backend.put('etag-bucket', 'f.txt', body, {})
        info = self.backend.head('etag-bucket', 'f.txt')
        expected = f'"{hashlib.md5(body).hexdigest()}"'
        assert info['ETag'] == expected
