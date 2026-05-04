# ═══════════════════════════════════════════════════════════════════════════════
# Tests — S3 Server service: test_S3_Server__Service
# Uses _Fake_S3_Server__Service subclass — no mocks, no AWS calls.
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                       import TestCase

from sg_compute_specs.s3_server.enums.Enum__S3_Server__Backend                     import Enum__S3_Server__Backend
from sg_compute_specs.s3_server.enums.Enum__S3_Server__Mode                        import Enum__S3_Server__Mode
from sg_compute_specs.s3_server.enums.Enum__S3_Server__Stack__State                import Enum__S3_Server__Stack__State
from sg_compute_specs.s3_server.schemas.Schema__S3_Server__Create__Request         import Schema__S3_Server__Create__Request
from sg_compute_specs.s3_server.schemas.Schema__S3_Server__Create__Response        import Schema__S3_Server__Create__Response
from sg_compute_specs.s3_server.schemas.Schema__S3_Server__Delete__Response        import Schema__S3_Server__Delete__Response
from sg_compute_specs.s3_server.schemas.Schema__S3_Server__Health__Response        import Schema__S3_Server__Health__Response
from sg_compute_specs.s3_server.schemas.Schema__S3_Server__List                    import Schema__S3_Server__List
from sg_compute_specs.s3_server.service.S3_Server__Service                         import S3_Server__Service
from sg_compute_specs.s3_server.service.S3_Server__Stack__Mapper                   import S3_Server__Stack__Mapper
from sg_compute_specs.s3_server.service.Random__Stack__Name__Generator             import Random__Stack__Name__Generator
from sg_compute_specs.s3_server.service.S3_Server__User_Data__Builder              import S3_Server__User_Data__Builder


class _Fake_Instance:
    def list_stacks(self, region): return {}
    def find_by_stack_name(self, region, stack_name): return None
    def terminate_instance(self, region, iid): return False


class _Fake_SG:
    def ensure_security_group(self, region, stack_name, caller_ip): return 'sg-fake0001'


class _Fake_AMI:
    def latest_al2023_ami_id(self, region): return 'ami-00000000000000001'


class _Fake_Launch:
    def run_instance(self, region, ami_id, sg_id, user_data, tags, instance_type='t3.small', instance_profile_name=None):
        return 'i-00000000000000001'


class _Fake_Tags:
    def build(self, stack_name, caller_ip, mode, creator=''):
        return [{'Key': 'Name', 'Value': f's3srv-{stack_name}'}]


class _Fake_IP_Detector:
    def detect(self): return '1.2.3.4'


class _Fake_Health_Checker:
    def check(self, region, stack_name, timeout_sec=0, poll_sec=10):
        return Schema__S3_Server__Health__Response(
            stack_name = stack_name,
            state      = Enum__S3_Server__Stack__State.UNKNOWN,
            message    = 'stack not found')


class _Fake_AWS_Client:
    sg       = _Fake_SG()
    ami      = _Fake_AMI()
    instance = _Fake_Instance()
    tags     = _Fake_Tags()
    launch   = _Fake_Launch()


class _Fake_S3_Server__Service(S3_Server__Service):
    def setup(self):
        self.aws_client        = _Fake_AWS_Client()
        self.mapper            = S3_Server__Stack__Mapper()
        self.ip_detector       = _Fake_IP_Detector()
        self.name_gen          = Random__Stack__Name__Generator()
        self.user_data_builder = S3_Server__User_Data__Builder()
        self.health_checker    = _Fake_Health_Checker()
        return self


class test_S3_Server__Service(TestCase):

    def setUp(self):
        self.service = _Fake_S3_Server__Service().setup()

    def test_create_returns_response_type(self):
        req  = Schema__S3_Server__Create__Request()
        resp = self.service.create_stack(req)
        assert isinstance(resp, Schema__S3_Server__Create__Response)

    def test_create_generates_stack_name_when_empty(self):
        req  = Schema__S3_Server__Create__Request()
        resp = self.service.create_stack(req)
        assert resp.stack_info is not None

    def test_create_uses_provided_stack_name(self):
        req      = Schema__S3_Server__Create__Request()
        req.stack_name = type('_FakeName', (), {'__str__': lambda s: 'fast-fermi'})()
        resp     = self.service.create_stack(req)
        assert resp.stack_info.instance_id != ''

    def test_list_returns_schema_list(self):
        result = self.service.list_stacks('eu-west-2')
        assert isinstance(result, Schema__S3_Server__List)
        assert result.total == 0

    def test_list_empty_when_no_instances(self):
        result = self.service.list_stacks('eu-west-2')
        assert len(result.stacks) == 0

    def test_get_stack_info_returns_none_for_missing(self):
        result = self.service.get_stack_info('eu-west-2', 'nonexistent')
        assert result is None

    def test_delete_returns_not_deleted_for_missing(self):
        resp = self.service.delete_stack('eu-west-2', 'nonexistent')
        assert isinstance(resp, Schema__S3_Server__Delete__Response)
        assert resp.deleted == False
        assert 'not found' in resp.message

    def test_health_returns_health_response(self):
        resp = self.service.health('eu-west-2', 'nonexistent', timeout_sec=0)
        assert isinstance(resp, Schema__S3_Server__Health__Response)
