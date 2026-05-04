# ═══════════════════════════════════════════════════════════════════════════════
# sg_s3_server — S3__XML__Error
# Builds AWS-format error envelopes. boto3 parses these on the client side.
# Unimplemented ops return HTTP 501 + NotImplemented; never 500, never HTML.
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.Type_Safe                                                import Type_Safe


class S3__XML__Error(Type_Safe):

    def not_implemented(self, operation: str = '') -> str:
        msg = f'The {operation} operation is not implemented by this server.' if operation else \
              'This operation is not implemented by this server.'
        return self._envelope('NotImplemented', msg)

    def no_such_bucket(self, bucket: str) -> str:
        return self._envelope('NoSuchBucket', f'The specified bucket does not exist: {bucket}')

    def no_such_key(self, bucket: str, key: str) -> str:
        return self._envelope('NoSuchKey', f'The specified key does not exist: {bucket}/{key}')

    def _envelope(self, code: str, message: str) -> str:
        return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
                f'<Error>'
                f'<Code>{code}</Code>'
                f'<Message>{message}</Message>'
                f'</Error>')
