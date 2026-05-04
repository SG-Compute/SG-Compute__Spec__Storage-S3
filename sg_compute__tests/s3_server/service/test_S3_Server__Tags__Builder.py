# ═══════════════════════════════════════════════════════════════════════════════
# Tests — S3 Server service: test_S3_Server__Tags__Builder
# Pure mapper — no AWS calls.
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                       import TestCase

from sg_compute_specs.s3_server.enums.Enum__S3_Server__Mode                        import Enum__S3_Server__Mode
from sg_compute_specs.s3_server.service.S3_Server__AWS__Client                     import (S3_SERVER_NAMING   ,
                                                                                              TAG_ALLOWED_IP_KEY ,
                                                                                              TAG_CREATOR_KEY    ,
                                                                                              TAG_MODE_KEY       ,
                                                                                              TAG_SECTION_KEY    ,
                                                                                              TAG_SECTION_VALUE  ,
                                                                                              TAG_STACK_NAME_KEY )
from sg_compute_specs.s3_server.service.S3_Server__Tags__Builder                   import S3_Server__Tags__Builder


class test_S3_Server__Tags__Builder(TestCase):

    def setUp(self):
        self.builder = S3_Server__Tags__Builder()

    def test_build__name_tag_carries_s3srv_prefix(self):
        tags    = self.builder.build('fast-fermi', '1.2.3.4')
        as_dict = {t['Key']: t['Value'] for t in tags}
        assert as_dict['Name'] == 's3srv-fast-fermi'

    def test_build__name_tag_does_not_double_prefix(self):
        tags    = self.builder.build('s3srv-fast-fermi', '1.2.3.4')
        as_dict = {t['Key']: t['Value'] for t in tags}
        assert as_dict['Name'] == 's3srv-fast-fermi'
        assert 's3srv-s3srv' not in as_dict['Name']

    def test_build__includes_section_tag(self):
        tags    = self.builder.build('cool-newton', '10.0.0.1')
        as_dict = {t['Key']: t['Value'] for t in tags}
        assert as_dict[TAG_SECTION_KEY]    == TAG_SECTION_VALUE
        assert as_dict[TAG_STACK_NAME_KEY] == 'cool-newton'
        assert as_dict[TAG_ALLOWED_IP_KEY] == '10.0.0.1'

    def test_build__mode_tag_present(self):
        tags    = self.builder.build('a-b', '1.2.3.4', Enum__S3_Server__Mode.FULL_PROXY)
        as_dict = {t['Key']: t['Value'] for t in tags}
        assert as_dict[TAG_MODE_KEY] == 'full-proxy'

    def test_build__creator_defaults_to_unknown(self):
        tags    = self.builder.build('a-b', '1.2.3.4')
        as_dict = {t['Key']: t['Value'] for t in tags}
        assert as_dict[TAG_CREATOR_KEY] == 'unknown'

    def test_build__creator_set(self):
        tags    = self.builder.build('a-b', '1.2.3.4', creator='dev@example.com')
        as_dict = {t['Key']: t['Value'] for t in tags}
        assert as_dict[TAG_CREATOR_KEY] == 'dev@example.com'

    def test_sg_name_never_starts_with_sg_prefix(self):
        sg_name = S3_SERVER_NAMING.sg_name_for_stack('fast-fermi')
        assert not sg_name.startswith('sg-')
        assert sg_name == 'fast-fermi-sg'
