# ═══════════════════════════════════════════════════════════════════════════════
# sg_s3_server — Call__Log__Middleware
# Starlette middleware that logs every request/response to an in-memory
# circular buffer (max 10 000 entries).
# ═══════════════════════════════════════════════════════════════════════════════

import time
from collections                                                                    import deque
from typing                                                                         import List

from starlette.middleware.base                                                      import BaseHTTPMiddleware
from starlette.requests                                                             import Request


MAX_ENTRIES = 10_000


def _derive_action(method: str, path: str, query: str) -> str:
    if 'Action=GetCallerIdentity' in query:
        return 'GetCallerIdentity'
    if method == 'GET'    and path == '/':
        return 'ListBuckets'
    if method == 'PUT'    and path.count('/') == 1:
        return 'CreateBucket'
    if method == 'GET'    and path.count('/') == 1:
        return 'ListObjectsV2'
    if method == 'PUT'    and path.count('/') >= 2:
        return 'PutObject'
    if method == 'GET'    and path.count('/') >= 2:
        return 'GetObject'
    if method == 'HEAD'   and path.count('/') >= 2:
        return 'HeadObject'
    if method == 'DELETE' and path.count('/') >= 2:
        return 'DeleteObject'
    return 'Unknown'


class Call__Log__Middleware(BaseHTTPMiddleware):
    log : deque

    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
        self.log = deque(maxlen=MAX_ENTRIES)

    async def dispatch(self, request: Request, call_next):
        t0     = time.time()
        method = request.method
        path   = request.url.path
        query  = str(request.url.query)
        action = _derive_action(method, path, query)

        response    = await call_next(request)
        elapsed_ms  = int((time.time() - t0) * 1000)
        status_code = response.status_code

        self.log.append({'timestamp'      : time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(t0)),
                         'method'         : method                                                ,
                         'path'           : path                                                  ,
                         'query'          : query                                                 ,
                         'aws_action'     : action                                                ,
                         'response_status': status_code                                           ,
                         'response_time_ms': elapsed_ms                                           })
        return response

    def entries(self) -> List[dict]:
        return list(self.log)
