# ═══════════════════════════════════════════════════════════════════════════════
# Tests — S3 Server: test_schemas
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                       import TestCase

from sg_compute_specs.s3_server.enums.Enum__S3_Server__Backend                     import Enum__S3_Server__Backend
from sg_compute_specs.s3_server.enums.Enum__S3_Server__Mode                        import Enum__S3_Server__Mode
from sg_compute_specs.s3_server.enums.Enum__S3_Server__Stack__State                import Enum__S3_Server__Stack__State
from sg_compute_specs.s3_server.schemas.Schema__S3_Server__Create__Request         import Schema__S3_Server__Create__Request
from sg_compute_specs.s3_server.schemas.Schema__S3_Server__Create__Response        import Schema__S3_Server__Create__Response
from sg_compute_specs.s3_server.schemas.Schema__S3_Server__Delete__Response        import Schema__S3_Server__Delete__Response
from sg_compute_specs.s3_server.schemas.Schema__S3_Server__Health__Response        import Schema__S3_Server__Health__Response
from sg_compute_specs.s3_server.schemas.Schema__S3_Server__Info                    import Schema__S3_Server__Info
from sg_compute_specs.s3_server.schemas.Schema__S3_Server__List                    import Schema__S3_Server__List


class test_schemas(TestCase):

    def test_create_request_default_mode(self):
        req = Schema__S3_Server__Create__Request()
        assert req.mode    == Enum__S3_Server__Mode.FULL_PROXY
        assert req.backend == Enum__S3_Server__Backend.MEMORY
        assert req.max_hours == 4

    def test_create_request_no_credential_fields(self):
        req   = Schema__S3_Server__Create__Request()
        attrs = vars(req)
        for field in attrs:
            assert 'secret' not in field.lower(), f'credential field found: {field}'
            assert 'password' not in field.lower()
            assert 'access_key' not in field.lower()

    def test_create_request_no_aws_secret_access_key(self):
        req = Schema__S3_Server__Create__Request()
        assert not hasattr(req, 'aws_secret_access_key')
        assert not hasattr(req, 'aws_access_key_id')

    def test_create_response_default_elapsed(self):
        resp = Schema__S3_Server__Create__Response()
        assert resp.elapsed_ms == 0

    def test_info_default_state(self):
        info = Schema__S3_Server__Info()
        assert info.state == Enum__S3_Server__Stack__State.UNKNOWN

    def test_info_has_url_fields(self):
        info = Schema__S3_Server__Info()
        assert hasattr(info, 's3_endpoint_url')
        assert hasattr(info, 'call_log_url')
        assert hasattr(info, 'ui_url')

    def test_delete_response_default_not_deleted(self):
        resp = Schema__S3_Server__Delete__Response()
        assert resp.deleted == False

    def test_health_response_default_not_healthy(self):
        resp = Schema__S3_Server__Health__Response()
        assert resp.healthy == False
        assert resp.state   == Enum__S3_Server__Stack__State.UNKNOWN

    def test_list_default_total(self):
        lst = Schema__S3_Server__List()
        assert lst.total == 0

    def test_info_spot_default_false(self):
        info = Schema__S3_Server__Info()
        assert info.spot == False
