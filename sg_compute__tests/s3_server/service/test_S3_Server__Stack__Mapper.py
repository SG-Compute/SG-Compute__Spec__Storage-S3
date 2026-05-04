# ═══════════════════════════════════════════════════════════════════════════════
# Tests — S3 Server service: test_S3_Server__Stack__Mapper
# Pure mapper — no AWS calls.
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                       import TestCase

from sg_compute_specs.s3_server.enums.Enum__S3_Server__Mode                        import Enum__S3_Server__Mode
from sg_compute_specs.s3_server.enums.Enum__S3_Server__Stack__State                import Enum__S3_Server__Stack__State
from sg_compute_specs.s3_server.schemas.Schema__S3_Server__Info                    import Schema__S3_Server__Info
from sg_compute_specs.s3_server.service.S3_Server__AWS__Client                     import TAG_ALLOWED_IP_KEY, TAG_MODE_KEY, TAG_STACK_NAME_KEY
from sg_compute_specs.s3_server.service.S3_Server__Stack__Mapper                   import S3_Server__Stack__Mapper


SAMPLE_DETAILS = {
    'InstanceId'     : 'i-0abc1234567890def',
    'ImageId'        : 'ami-0123456789abcdef0',
    'InstanceType'   : 't3.small',
    'State'          : {'Name': 'running'},
    'PublicIpAddress': '54.1.2.3',
    'LaunchTime'     : '2026-05-04T12:00:00+00:00',
    'SecurityGroups' : [{'GroupId': 'sg-0123456789abcdef0'}],
    'Tags'           : [
        {'Key': 'Name'            , 'Value': 's3srv-fast-fermi'},
        {'Key': TAG_STACK_NAME_KEY, 'Value': 'fast-fermi'      },
        {'Key': TAG_ALLOWED_IP_KEY, 'Value': '10.0.0.1'        },
        {'Key': TAG_MODE_KEY      , 'Value': 'full-proxy'       },
    ],
}


class test_S3_Server__Stack__Mapper(TestCase):

    def setUp(self):
        self.mapper = S3_Server__Stack__Mapper()

    def test_to_info__returns_schema_info(self):
        info = self.mapper.to_info(SAMPLE_DETAILS, 'eu-west-2')
        assert isinstance(info, Schema__S3_Server__Info)

    def test_to_info__stack_name(self):
        info = self.mapper.to_info(SAMPLE_DETAILS, 'eu-west-2')
        assert str(info.stack_name) == 'fast-fermi'

    def test_to_info__state_ready_for_running(self):
        info = self.mapper.to_info(SAMPLE_DETAILS, 'eu-west-2')
        assert info.state == Enum__S3_Server__Stack__State.READY

    def test_to_info__state_terminated(self):
        details = {**SAMPLE_DETAILS, 'State': {'Name': 'terminated'}}
        info    = self.mapper.to_info(details, 'eu-west-2')
        assert info.state == Enum__S3_Server__Stack__State.TERMINATED

    def test_to_info__state_shutting_down_maps_to_terminating(self):
        details = {**SAMPLE_DETAILS, 'State': {'Name': 'shutting-down'}}
        info    = self.mapper.to_info(details, 'eu-west-2')
        assert info.state == Enum__S3_Server__Stack__State.TERMINATING

    def test_to_info__mode_from_tag(self):
        info = self.mapper.to_info(SAMPLE_DETAILS, 'eu-west-2')
        assert info.mode == Enum__S3_Server__Mode.FULL_PROXY

    def test_to_info__s3_endpoint_url_built_from_public_ip(self):
        info = self.mapper.to_info(SAMPLE_DETAILS, 'eu-west-2')
        assert info.s3_endpoint_url == 'http://54.1.2.3:9000'

    def test_to_info__call_log_url_built(self):
        info = self.mapper.to_info(SAMPLE_DETAILS, 'eu-west-2')
        assert info.call_log_url == 'http://54.1.2.3:9000/call-log'

    def test_to_info__ui_url_built(self):
        info = self.mapper.to_info(SAMPLE_DETAILS, 'eu-west-2')
        assert info.ui_url == 'http://54.1.2.3:9000/ui/'

    def test_to_info__empty_details_returns_unknown_state(self):
        info = self.mapper.to_info({}, 'eu-west-2')
        assert info.state == Enum__S3_Server__Stack__State.UNKNOWN

    def test_to_info__no_public_ip_gives_empty_urls(self):
        details = {k: v for k, v in SAMPLE_DETAILS.items() if k != 'PublicIpAddress'}
        info    = self.mapper.to_info(details, 'eu-west-2')
        assert info.s3_endpoint_url == ''
        assert info.call_log_url    == ''
        assert info.ui_url          == ''
