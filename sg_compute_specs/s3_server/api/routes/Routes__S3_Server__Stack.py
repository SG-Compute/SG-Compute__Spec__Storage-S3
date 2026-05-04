# ═══════════════════════════════════════════════════════════════════════════════
# SG/Compute Specs — S3 Server: Routes__S3_Server__Stack
# HTTP surface for the S3 server compute spec. Zero logic — delegates to
# S3_Server__Service.
#
# Endpoints
# ─────────
#   POST   /api/specs/s3_server/stack                -> Schema__S3_Server__Create__Response
#   GET    /api/specs/s3_server/stacks               -> Schema__S3_Server__List
#   GET    /api/specs/s3_server/stack/{name}         -> Schema__S3_Server__Info
#   DELETE /api/specs/s3_server/stack/{name}         -> Schema__S3_Server__Delete__Response
#   GET    /api/specs/s3_server/stack/{name}/health  -> Schema__S3_Server__Health__Response
# ═══════════════════════════════════════════════════════════════════════════════

from fastapi                                                                        import HTTPException

from osbot_fast_api.api.routes.Fast_API__Routes                                     import Fast_API__Routes

from sg_compute_specs.s3_server.schemas.Schema__S3_Server__Create__Request         import Schema__S3_Server__Create__Request
from sg_compute_specs.s3_server.service.S3_Server__Service                         import DEFAULT_REGION, S3_Server__Service


TAG__ROUTES_S3_SERVER = 's3_server'


class Routes__S3_Server__Stack(Fast_API__Routes):
    tag     : str              = TAG__ROUTES_S3_SERVER
    service : S3_Server__Service

    def list_stacks(self, region: str = '') -> dict:                                # GET /api/specs/s3_server/stacks
        return self.service.list_stacks(region or DEFAULT_REGION).json()
    list_stacks.__route_path__ = '/stacks'

    def info(self, name: str, region: str = '') -> dict:                            # GET /api/specs/s3_server/stack/{name}
        result = self.service.get_stack_info(region or DEFAULT_REGION, name)
        if result is None:
            raise HTTPException(status_code=404, detail=f'no s3_server stack matched {name!r}')
        return result.json()
    info.__route_path__ = '/stack/{name}'

    def create(self, body: Schema__S3_Server__Create__Request) -> dict:             # POST /api/specs/s3_server/stack
        return self.service.create_stack(body).json()
    create.__route_path__ = '/stack'

    def delete(self, name: str, region: str = '') -> dict:                          # DELETE /api/specs/s3_server/stack/{name}
        response = self.service.delete_stack(region or DEFAULT_REGION, name)
        if not response.deleted:
            raise HTTPException(status_code=404, detail=f'no s3_server stack matched {name!r}')
        return response.json()
    delete.__route_path__ = '/stack/{name}'

    def health(self, name: str, region: str = '') -> dict:                          # GET /api/specs/s3_server/stack/{name}/health
        return self.service.health(region or DEFAULT_REGION, name, timeout_sec=0).json()
    health.__route_path__ = '/stack/{name}/health'

    def setup_routes(self):
        self.add_route_get   (self.list_stacks)
        self.add_route_get   (self.info       )
        self.add_route_post  (self.create     )
        self.add_route_delete(self.delete     )
        self.add_route_get   (self.health     )
