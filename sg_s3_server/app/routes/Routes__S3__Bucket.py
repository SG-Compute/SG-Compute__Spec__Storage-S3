# ═══════════════════════════════════════════════════════════════════════════════
# sg_s3_server — Routes__S3__Bucket
# PUT /{bucket}          → CreateBucket
# GET /                  → ListBuckets
# GET /{bucket}          → ListObjectsV2
# ═══════════════════════════════════════════════════════════════════════════════

from fastapi                                                                        import Request, Response
from fastapi.routing                                                                import APIRouter

from sg_s3_server.backends.S3__Backend                                             import S3__Backend
from sg_s3_server.xml.S3__XML__Error                                               import S3__XML__Error
from sg_s3_server.xml.S3__XML__Response                                            import S3__XML__Response

XML_CONTENT_TYPE = 'application/xml'

xml_response = S3__XML__Response()
xml_error    = S3__XML__Error()


def make_bucket_router(backend: S3__Backend) -> APIRouter:
    router = APIRouter()

    @router.get('/')
    async def list_buckets(request: Request):
        action = request.query_params.get('Action', '')
        if action == 'GetCallerIdentity':
            body = xml_response.sts_get_caller_identity()
            return Response(content=body, media_type=XML_CONTENT_TYPE)
        buckets = backend.list_buckets()
        body    = xml_response.list_buckets(buckets)
        return Response(content=body, media_type=XML_CONTENT_TYPE)

    @router.put('/{bucket}')
    async def create_bucket(bucket: str):
        backend.create_bucket(bucket)
        return Response(status_code=200)

    @router.get('/{bucket}')
    async def list_objects(bucket: str, request: Request):
        prefix   = request.query_params.get('prefix', '')
        max_keys = int(request.query_params.get('max-keys', 1000))
        objects  = backend.list(bucket, prefix, max_keys)
        body     = xml_response.list_objects_v2(bucket, objects, prefix, max_keys)
        return Response(content=body, media_type=XML_CONTENT_TYPE)

    return router
