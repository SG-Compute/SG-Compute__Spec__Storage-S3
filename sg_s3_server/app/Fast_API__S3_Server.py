# ═══════════════════════════════════════════════════════════════════════════════
# sg_s3_server — Fast_API__S3_Server
# FastAPI application. Wires backend, call-log middleware, and S3 routes.
# Environment variables:
#   S3_SERVER_MODE    — 'full-proxy' | 'full-local' | 'hybrid' | 'selective'
#   S3_SERVER_BACKEND — 'memory' | 'disk' | 'real-s3'
# ═══════════════════════════════════════════════════════════════════════════════

import os
from pathlib                                                                        import Path

from fastapi                                                                        import FastAPI
from fastapi.staticfiles                                                            import StaticFiles

from sg_s3_server.backends.S3__Backend__Memory                                     import S3__Backend__Memory


def _build_backend():                                                               # Phase 1: always memory regardless of env vars
    backend = S3__Backend__Memory()
    backend.setup()
    return backend


def create_app(backend=None) -> FastAPI:
    from sg_s3_server.app.middleware.Call__Log__Middleware                         import Call__Log__Middleware
    from sg_s3_server.app.routes.Routes__S3__Bucket                                import make_bucket_router
    from sg_s3_server.app.routes.Routes__S3__Call_Log                              import make_call_log_router
    from sg_s3_server.app.routes.Routes__S3__Object                                import make_object_router

    if backend is None:
        backend = _build_backend()

    call_log = Call__Log__Middleware.__new__(Call__Log__Middleware)
    call_log.__init_raw__() if hasattr(call_log, '__init_raw__') else None

    fast_api = FastAPI(title='SG S3 Server', version='0.1.0')

    call_log_store = {'mw': None}

    class _MW(Call__Log__Middleware):                                               # thin subclass to capture the live instance
        def __init__(self, inner_app, **kwargs):
            super().__init__(inner_app, **kwargs)
            call_log_store['mw'] = self

    fast_api.add_middleware(_MW)

    class _LogProxy:                                                                # proxy so routers see the middleware after startup
        def entries(self):
            mw = call_log_store.get('mw')
            return mw.entries() if mw else []
        @property
        def log(self):
            mw = call_log_store.get('mw')
            return mw.log if mw else []

    fast_api.include_router(make_call_log_router(_LogProxy()))
    fast_api.include_router(make_bucket_router(backend))
    fast_api.include_router(make_object_router(backend))

    static_dir = Path(__file__).parent.parent / 'ui' / 'static'
    if static_dir.exists():
        fast_api.mount('/ui', StaticFiles(directory=str(static_dir), html=True), name='ui')

    return fast_api


app = create_app()
