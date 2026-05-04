# ═══════════════════════════════════════════════════════════════════════════════
# SG/Compute Specs — S3 Server: Schema__S3_Server__Create__Response
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text        import Safe_Str__Text

from sg_compute_specs.s3_server.schemas.Schema__S3_Server__Info                    import Schema__S3_Server__Info


class Schema__S3_Server__Create__Response(Type_Safe):
    stack_info : Schema__S3_Server__Info
    message    : Safe_Str__Text
    elapsed_ms : int = 0
