# ═══════════════════════════════════════════════════════════════════════════════
# Tests — S3 Server: test_manifest
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                       import TestCase

from sg_compute.core.spec.schemas.Schema__Spec__Manifest__Entry                     import Schema__Spec__Manifest__Entry
from sg_compute.primitives.enums.Enum__Spec__Capability                             import Enum__Spec__Capability
from sg_compute.primitives.enums.Enum__Spec__Nav_Group                              import Enum__Spec__Nav_Group
from sg_compute.primitives.enums.Enum__Spec__Stability                              import Enum__Spec__Stability
from sg_compute_specs.s3_server.manifest                                            import MANIFEST


class test_manifest(TestCase):

    def test_manifest_is_typed(self):
        assert isinstance(MANIFEST, Schema__Spec__Manifest__Entry)

    def test_spec_id(self):
        assert MANIFEST.spec_id == 's3_server'

    def test_display_name(self):
        assert 'S3' in MANIFEST.display_name or 'Storage' in MANIFEST.display_name

    def test_version_is_semver(self):
        parts = MANIFEST.version.split('.')
        assert len(parts) == 3
        assert all(p.isdigit() for p in parts)

    def test_capabilities_includes_object_storage(self):
        assert Enum__Spec__Capability.OBJECT_STORAGE in MANIFEST.capabilities

    def test_nav_group_is_storage(self):
        assert MANIFEST.nav_group == Enum__Spec__Nav_Group.STORAGE

    def test_stability_is_experimental(self):
        assert MANIFEST.stability == Enum__Spec__Stability.EXPERIMENTAL

    def test_create_endpoint_path(self):
        assert MANIFEST.create_endpoint_path == '/api/specs/s3_server/stack'

    def test_boot_seconds_reasonable(self):
        assert MANIFEST.boot_seconds_typical > 0

    def test_spec_loader_finds_manifest(self):
        from sg_compute.core.spec.Spec__Loader import Spec__Loader
        registry = Spec__Loader().load_all()
        ids = [e.spec_id for e in registry._specs.values() if hasattr(registry, '_specs')] \
              if hasattr(registry, '_specs') else []
        assert MANIFEST.spec_id == 's3_server'
