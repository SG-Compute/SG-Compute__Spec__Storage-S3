# ═══════════════════════════════════════════════════════════════════════════════
# sg_s3_server — S3__Backend
# Abstract storage backend. Subclass and override all methods.
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.Type_Safe                                                import Type_Safe


class S3__Backend(Type_Safe):

    def put(self, bucket: str, key: str, body: bytes, metadata: dict) -> None:
        raise NotImplementedError

    def get(self, bucket: str, key: str) -> bytes:
        raise NotImplementedError

    def head(self, bucket: str, key: str) -> dict:
        raise NotImplementedError

    def delete(self, bucket: str, key: str) -> None:
        raise NotImplementedError

    def list(self, bucket: str, prefix: str = '', max_keys: int = 1000) -> list:
        raise NotImplementedError

    def create_bucket(self, bucket: str) -> None:
        raise NotImplementedError

    def list_buckets(self) -> list:
        raise NotImplementedError
