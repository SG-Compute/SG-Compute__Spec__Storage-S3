# ═══════════════════════════════════════════════════════════════════════════════
# sg_s3_server — Routes__S3__Call_Log
# GET /call-log  → JSON feed of recent requests (polled by browser UI)
# GET /health    → {"status": "ok"}
# ═══════════════════════════════════════════════════════════════════════════════

from fastapi                                                                        import Request
from fastapi.responses                                                              import JSONResponse
from fastapi.routing                                                                import APIRouter


def make_call_log_router(middleware_ref) -> APIRouter:
    router = APIRouter()

    @router.get('/health')
    async def health():
        return JSONResponse({'status': 'ok'})

    @router.get('/call-log')
    async def call_log(request: Request):
        limit   = int(request.query_params.get('limit', 200))
        entries = middleware_ref.entries()[-limit:]
        return JSONResponse({'entries': entries, 'total': len(middleware_ref.log)})

    return router
