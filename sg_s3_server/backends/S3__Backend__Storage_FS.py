# ═══════════════════════════════════════════════════════════════════════════════
# sg_s3_server — S3__Backend__Storage_FS
# Memory-FS adapter. Maps S3 bucket/key → Storage_FS flat path.
# Bucket registry kept in __buckets__.json within the same storage.
# Thread safety: RLock guards writes; reads are lock-free.
# ═══════════════════════════════════════════════════════════════════════════════

import hashlib
import json
import threading

from datetime                                                                       import datetime
from typing                                                                         import Optional

from sg_s3_server.backends.S3__Backend                                             import S3__Backend


class S3__Backend__Storage_FS(S3__Backend):
    storage        : object = None                                                  # Storage_FS instance
    _registry_path : str    = '__buckets__.json'
    _lock          : object = None

    def setup(self, storage_type: str = 'memory', **config) -> 'S3__Backend__Storage_FS':
        from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path import Safe_Str__File__Path
        self._path_cls = Safe_Str__File__Path
        self._lock     = threading.RLock()

        if storage_type == 'memory':
            from memory_fs.storage_fs.Storage_FS__Memory import Storage_FS__Memory  # noqa: F401
            self.storage = Storage_FS__Memory()
        elif storage_type == 's3':
            from memory_fs.storage_fs.Storage_FS__S3 import Storage_FS__S3          # noqa: F401
            self.storage = Storage_FS__S3(s3_bucket=config.get('s3_bucket', ''),
                                          s3_prefix=config.get('s3_prefix', ''))
            self.storage.setup()
        else:
            raise ValueError(f'unknown storage_type: {storage_type!r}')
        return self

    def _path(self, bucket: str, key: str):
        return self._path_cls(f'{bucket}/{key}')

    def _read_registry(self) -> list:
        reg_path = self._path_cls(self._registry_path)
        if self.storage.file__exists(reg_path):
            data = self.storage.file__json(reg_path)
            return data.get('buckets', []) if data else []
        return []

    def _write_registry(self, buckets: list):
        reg_path = self._path_cls(self._registry_path)
        self.storage.file__save(reg_path, json.dumps({'buckets': buckets}).encode())

    def put(self, bucket: str, key: str, body: bytes, metadata: dict) -> None:
        with self._lock:
            self.create_bucket(bucket)
            path = self._path(bucket, key)
            self.storage.file__save(path, body)
            if metadata:
                storage_meta = {'ContentType'  : metadata.get('Content-Type', 'binary/octet-stream'),
                                'UserMetadata' : {k[11:]: v for k, v in metadata.items()
                                                  if k.startswith('x-amz-meta-')},
                                'UploadTime'   : datetime.utcnow().isoformat()}
                self.storage.file__metadata_update(path, storage_meta)

    def get(self, bucket: str, key: str) -> Optional[bytes]:
        return self.storage.file__bytes(self._path(bucket, key))

    def head(self, bucket: str, key: str) -> Optional[dict]:
        path = self._path(bucket, key)
        if not self.storage.file__exists(path):
            return None
        meta  = self.storage.file__metadata(path) or {}
        size  = self.storage.file__size(path) or 0
        mtime = self.storage.file__last_modified(path) or datetime.utcnow().isoformat()
        body  = self.storage.file__bytes(path)
        etag  = hashlib.md5(body).hexdigest() if body else ''
        return {'ContentType'  : meta.get('ContentType', 'binary/octet-stream'),
                'ContentLength': size                                            ,
                'ETag'         : f'"{etag}"'                                    ,
                'LastModified' : mtime                                          ,
                'Metadata'     : meta.get('UserMetadata', {})                   }

    def delete(self, bucket: str, key: str) -> None:
        self.storage.file__delete(self._path(bucket, key))

    def list(self, bucket: str, prefix: str = '', max_keys: int = 1000) -> list:
        bucket_prefix = f'{bucket}/'
        all_paths     = self.storage.files__paths()
        results       = []
        for p in all_paths:
            s = str(p)
            if not s.startswith(bucket_prefix):
                continue
            if str(p) == self._registry_path:
                continue
            key = s[len(bucket_prefix):]
            if prefix and not key.startswith(prefix):
                continue
            size  = self.storage.file__size(p) or 0
            mtime = self.storage.file__last_modified(p) or ''
            results.append({'Key': key, 'Size': size, 'LastModified': mtime})
            if len(results) >= max_keys:
                break
        return results

    def create_bucket(self, bucket: str) -> None:
        with self._lock:
            buckets = self._read_registry()
            if bucket not in buckets:
                buckets.append(bucket)
                self._write_registry(buckets)

    def list_buckets(self) -> list:
        return [{'Name': b} for b in self._read_registry()]
