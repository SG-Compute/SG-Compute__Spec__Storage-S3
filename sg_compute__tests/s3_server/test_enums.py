# ═══════════════════════════════════════════════════════════════════════════════
# Tests — S3 Server: test_enums
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                       import TestCase

from sg_compute_specs.s3_server.enums.Enum__S3_Server__Mode                        import Enum__S3_Server__Mode
from sg_compute_specs.s3_server.enums.Enum__S3_Server__Backend                     import Enum__S3_Server__Backend
from sg_compute_specs.s3_server.enums.Enum__S3_Server__Stack__State                import Enum__S3_Server__Stack__State
from sg_compute_specs.s3_server.enums.Enum__S3__Handler                            import Enum__S3__Handler


class test_enums(TestCase):

    def test_mode_values(self):
        assert Enum__S3_Server__Mode.FULL_LOCAL.value == 'full-local'
        assert Enum__S3_Server__Mode.FULL_PROXY.value == 'full-proxy'
        assert Enum__S3_Server__Mode.HYBRID.value     == 'hybrid'
        assert Enum__S3_Server__Mode.SELECTIVE.value  == 'selective'

    def test_mode_all_four_values_present(self):
        assert len(Enum__S3_Server__Mode) == 4

    def test_backend_values(self):
        assert Enum__S3_Server__Backend.MEMORY.value  == 'memory'
        assert Enum__S3_Server__Backend.DISK.value    == 'disk'
        assert Enum__S3_Server__Backend.VAULT.value   == 'vault'
        assert Enum__S3_Server__Backend.REAL_S3.value == 'real-s3'

    def test_stack_state_values(self):
        states = {s.value for s in Enum__S3_Server__Stack__State}
        assert 'pending'     in states
        assert 'ready'       in states
        assert 'terminating' in states
        assert 'terminated'  in states
        assert 'failed'      in states
        assert 'unknown'     in states

    def test_handler_values(self):
        assert Enum__S3__Handler.LOCAL.value    == 'local'
        assert Enum__S3__Handler.PROXY.value    == 'proxy'
        assert Enum__S3__Handler.NOT_IMPL.value == 'not-impl'

    def test_mode_is_str_enum(self):
        assert isinstance(Enum__S3_Server__Mode.FULL_PROXY, str)
        assert str(Enum__S3_Server__Mode.FULL_PROXY) == 'full-proxy'

    def test_backend_is_str_enum(self):
        assert isinstance(Enum__S3_Server__Backend.MEMORY, str)
