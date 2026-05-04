# ═══════════════════════════════════════════════════════════════════════════════
# Tests — S3 Server service: test_S3_Server__User_Data__Builder
# Pure template renderer — no AWS calls.
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                       import TestCase

from sg_compute_specs.s3_server.service.S3_Server__User_Data__Builder              import (S3_Server__User_Data__Builder,
                                                                                              PLACEHOLDERS               )


class test_S3_Server__User_Data__Builder(TestCase):

    def setUp(self):
        self.builder = S3_Server__User_Data__Builder()

    def test_render__starts_with_shebang(self):
        result = self.builder.render('fast-fermi', 'eu-west-2')
        assert result.startswith('#!/usr/bin/env bash')

    def test_render__installs_docker(self):
        result = self.builder.render('fast-fermi', 'eu-west-2')
        assert 'dnf install -y docker' in result

    def test_render__starts_s3_server_container(self):
        result = self.builder.render('fast-fermi', 'eu-west-2')
        assert 'sg-s3-server' in result
        assert '9000:9000' in result

    def test_render__embeds_stack_name_and_region(self):
        result = self.builder.render('fast-fermi', 'eu-west-2')
        assert 'fast-fermi' in result
        assert 'eu-west-2'  in result

    def test_render__no_aws_credentials(self):
        result = self.builder.render('fast-fermi', 'eu-west-2')
        assert 'aws_secret_access_key' not in result.lower()
        assert 'aws_access_key_id'     not in result.lower()
        assert 'secretaccesskey'       not in result.lower()

    def test_render__mode_embedded(self):
        result = self.builder.render('a-b', 'eu-west-2', mode='full-proxy')
        assert 'full-proxy' in result

    def test_render__backend_embedded(self):
        result = self.builder.render('a-b', 'eu-west-2', backend='memory')
        assert 'memory' in result

    def test_render__shutdown_included_when_max_hours_set(self):
        result = self.builder.render('a-b', 'eu-west-2', max_hours=4)
        assert 'shutdown -h +240' in result

    def test_render__no_shutdown_when_max_hours_zero(self):
        result = self.builder.render('a-b', 'eu-west-2', max_hours=0)
        assert 'shutdown -h' not in result
        assert 'no auto-terminate' in result

    def test_placeholders_locked(self):
        assert 'stack_name'       in PLACEHOLDERS
        assert 'region'           in PLACEHOLDERS
        assert 'mode'             in PLACEHOLDERS
        assert 'backend'          in PLACEHOLDERS
        assert 'shutdown_line'    in PLACEHOLDERS

    def test_create_request_default_max_hours(self):
        from sg_compute_specs.s3_server.schemas.Schema__S3_Server__Create__Request import Schema__S3_Server__Create__Request
        assert Schema__S3_Server__Create__Request().max_hours == 4

    def test_create_request_default_mode_is_full_proxy(self):
        from sg_compute_specs.s3_server.schemas.Schema__S3_Server__Create__Request import Schema__S3_Server__Create__Request
        from sg_compute_specs.s3_server.enums.Enum__S3_Server__Mode import Enum__S3_Server__Mode
        assert Schema__S3_Server__Create__Request().mode == Enum__S3_Server__Mode.FULL_PROXY
