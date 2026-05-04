# ═══════════════════════════════════════════════════════════════════════════════
# Tests — S3 Server: test_primitives
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                       import TestCase

from sg_compute_specs.s3_server.primitives.Safe_Str__S3_Server__Stack__Name        import Safe_Str__S3_Server__Stack__Name
from sg_compute_specs.s3_server.primitives.Safe_Str__IP__Address                   import Safe_Str__IP__Address


class test_primitives(TestCase):

    def test_stack_name_valid(self):
        name = Safe_Str__S3_Server__Stack__Name('fast-fermi')
        assert str(name) == 'fast-fermi'

    def test_stack_name_valid_with_numbers(self):
        name = Safe_Str__S3_Server__Stack__Name('cool-node42')
        assert str(name) == 'cool-node42'

    def test_stack_name_empty_allowed(self):
        name = Safe_Str__S3_Server__Stack__Name('')
        assert str(name) == ''

    def test_stack_name_invalid_starts_with_digit(self):
        try:
            Safe_Str__S3_Server__Stack__Name('1bad')
            assert False, 'should have raised'
        except Exception:
            pass

    def test_stack_name_invalid_uppercase(self):
        try:
            Safe_Str__S3_Server__Stack__Name('Fast-Fermi')
            assert False, 'should have raised'
        except Exception:
            pass

    def test_stack_name_too_long(self):
        try:
            Safe_Str__S3_Server__Stack__Name('a' * 65)
            assert False, 'should have raised'
        except Exception:
            pass

    def test_ip_address_valid(self):
        ip = Safe_Str__IP__Address('1.2.3.4')
        assert str(ip) == '1.2.3.4'

    def test_ip_address_valid_public(self):
        ip = Safe_Str__IP__Address('54.123.45.67')
        assert str(ip) == '54.123.45.67'

    def test_ip_address_empty_allowed(self):
        ip = Safe_Str__IP__Address('')
        assert str(ip) == ''

    def test_ip_address_invalid_letters(self):
        try:
            Safe_Str__IP__Address('not.an.ip.address')
            assert False, 'should have raised'
        except Exception:
            pass
