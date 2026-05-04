# ═══════════════════════════════════════════════════════════════════════════════
# sg_s3_server — Routes__S3__Object
# PUT    /{bucket}/{key+}   → PutObject
# GET    /{bucket}/{key+}   → GetObject
# HEAD   /{bucket}/{key+}   → HeadObject
# DELETE /{bucket}/{key+}   → DeleteObject
# ═══════════════════════════════════════════════════════════════════════════════

from fastapi                                                                        import Request, Response
from fastapi.routing                                                                import APIRouter

from sg_s3_server.backends.S3__Backend                                             import S3__Backend
from sg_s3_server.xml.S3__XML__Error                                               import S3__XML__Error

XML_CONTENT_TYPE = 'application/xml'

xml_error = S3__XML__Error()


def make_object_router(backend: S3__Backend) -> APIRouter:
    router = APIRouter()

    @router.put('/{bucket}/{key:path}')
    async def put_object(bucket: str, key: str, request: Request):
        body     = await request.body()
        metadata = dict(request.headers)
        backend.put(bucket, key, body, metadata)
        return Response(status_code=200)

    @router.get('/{bucket}/{key:path}')
    async def get_object(bucket: str, key: str):
        data = backend.get(bucket, key)
        if data is None:
            return Response(content=xml_error.no_such_key(bucket, key),
                            status_code=404, media_type=XML_CONTENT_TYPE)
        return Response(content=data, media_type='application/octet-stream')

    @router.head('/{bucket}/{key:path}')
    async def head_object(bucket: str, key: str):
        info = backend.head(bucket, key)
        if info is None:
            return Response(content=xml_error.no_such_key(bucket, key),
                            status_code=404, media_type=XML_CONTENT_TYPE)
        headers = {'Content-Length' : str(info.get('ContentLength', 0)),
                   'Content-Type'   : info.get('ContentType', 'binary/octet-stream'),
                   'ETag'           : info.get('ETag', ''),
                   'Last-Modified'  : str(info.get('LastModified', ''))}
        return Response(status_code=200, headers=headers)

    @router.delete('/{bucket}/{key:path}')
    async def delete_object(bucket: str, key: str):
        backend.delete(bucket, key)
        return Response(status_code=204)

    return router
