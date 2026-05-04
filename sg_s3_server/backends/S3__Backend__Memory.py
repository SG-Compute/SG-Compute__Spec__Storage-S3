# ═══════════════════════════════════════════════════════════════════════════════
# sg_s3_server — S3__Backend__Memory
# Phase 1 default backend. In-process dict, no persistence.
# Thread safety: a single RLock guards all writes; reads are lock-free.
# ═══════════════════════════════════════════════════════════════════════════════

import hashlib
import threading
import time

from typing                                                                         import Optional

from sg_s3_server.backends.S3__Backend                                             import S3__Backend


class S3__Backend__Memory(S3__Backend):
    _objects  : dict = None                                                         # {bucket: {key: {'body': bytes, 'metadata': dict, 'mtime': float}}}
    _buckets  : list = None
    _lock     : object = None

    def setup(self) -> 'S3__Backend__Memory':
        self._objects = {}
        self._buckets = []
        self._lock    = threading.RLock()
        return self

    def _ensure_setup(self):
        if self._objects is None:
            self.setup()

    def put(self, bucket: str, key: str, body: bytes, metadata: dict) -> None:
        self._ensure_setup()
        with self._lock:
            if bucket not in self._objects:
                self._objects[bucket] = {}
                if bucket not in self._buckets:
                    self._buckets.append(bucket)
            self._objects[bucket][key] = {'body': body, 'metadata': metadata or {}, 'mtime': time.time()}

    def get(self, bucket: str, key: str) -> Optional[bytes]:
        self._ensure_setup()
        entry = self._objects.get(bucket, {}).get(key)
        return entry['body'] if entry else None

    def head(self, bucket: str, key: str) -> Optional[dict]:
        self._ensure_setup()
        entry = self._objects.get(bucket, {}).get(key)
        if not entry:
            return None
        body  = entry['body']
        etag  = hashlib.md5(body).hexdigest() if body else ''
        meta  = entry.get('metadata', {})
        return {'ContentType'  : meta.get('Content-Type', 'binary/octet-stream'),
                'ContentLength': len(body)                                        ,
                'ETag'         : f'"{etag}"'                                      ,
                'LastModified' : str(entry.get('mtime', ''))                      ,
                'Metadata'     : {k[11:]: v for k, v in meta.items()
                                  if k.startswith('x-amz-meta-')}                }

    def delete(self, bucket: str, key: str) -> None:
        self._ensure_setup()
        with self._lock:
            if bucket in self._objects and key in self._objects[bucket]:
                del self._objects[bucket][key]

    def list(self, bucket: str, prefix: str = '', max_keys: int = 1000) -> list:
        self._ensure_setup()
        bucket_keys = self._objects.get(bucket, {})
        results = []
        for key, entry in bucket_keys.items():
            if not prefix or key.startswith(prefix):
                body = entry['body']
                results.append({'Key'         : key                     ,
                                'Size'        : len(body) if body else 0,
                                'LastModified': str(entry.get('mtime', ''))})
                if len(results) >= max_keys:
                    break
        return results

    def create_bucket(self, bucket: str) -> None:
        self._ensure_setup()
        with self._lock:
            if bucket not in self._buckets:
                self._buckets.append(bucket)
            if bucket not in self._objects:
                self._objects[bucket] = {}

    def list_buckets(self) -> list:
        self._ensure_setup()
        return [{'Name': b} for b in self._buckets]
