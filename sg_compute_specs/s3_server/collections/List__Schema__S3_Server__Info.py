# ═══════════════════════════════════════════════════════════════════════════════
# SG/Compute Specs — S3 Server: List__Schema__S3_Server__Info
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List              import Type_Safe__List

from sg_compute_specs.s3_server.schemas.Schema__S3_Server__Info                    import Schema__S3_Server__Info


class List__Schema__S3_Server__Info(Type_Safe__List):
    expected_type = Schema__S3_Server__Info
