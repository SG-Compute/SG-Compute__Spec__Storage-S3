# ═══════════════════════════════════════════════════════════════════════════════
# SG/Compute Specs — S3 Server: Schema__S3_Server__Health__Response
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text        import Safe_Str__Text

from sg_compute_specs.s3_server.enums.Enum__S3_Server__Stack__State                import Enum__S3_Server__Stack__State
from sg_compute_specs.s3_server.primitives.Safe_Str__S3_Server__Stack__Name        import Safe_Str__S3_Server__Stack__Name


class Schema__S3_Server__Health__Response(Type_Safe):
    stack_name : Safe_Str__S3_Server__Stack__Name
    state      : Enum__S3_Server__Stack__State = Enum__S3_Server__Stack__State.UNKNOWN
    healthy    : bool = False
    message    : Safe_Str__Text
    elapsed_ms : int  = 0
