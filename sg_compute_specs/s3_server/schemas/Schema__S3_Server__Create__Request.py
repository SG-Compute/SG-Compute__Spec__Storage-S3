# ═══════════════════════════════════════════════════════════════════════════════
# SG/Compute Specs — S3 Server: Schema__S3_Server__Create__Request
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text        import Safe_Str__Text

from sgraph_ai_service_playwright__cli.ec2.primitives.Safe_Str__AMI__Id             import Safe_Str__AMI__Id
from sgraph_ai_service_playwright__cli.observability.primitives.Safe_Str__AWS__Region import Safe_Str__AWS__Region

from sg_compute_specs.s3_server.enums.Enum__S3_Server__Backend                     import Enum__S3_Server__Backend
from sg_compute_specs.s3_server.enums.Enum__S3_Server__Mode                        import Enum__S3_Server__Mode
from sg_compute_specs.s3_server.primitives.Safe_Str__IP__Address                   import Safe_Str__IP__Address
from sg_compute_specs.s3_server.primitives.Safe_Str__S3_Server__Stack__Name        import Safe_Str__S3_Server__Stack__Name


class Schema__S3_Server__Create__Request(Type_Safe):
    stack_name        : Safe_Str__S3_Server__Stack__Name
    region            : Safe_Str__AWS__Region
    instance_type     : Safe_Str__Text                  = 't3.small'
    from_ami          : Safe_Str__AMI__Id
    caller_ip         : Safe_Str__IP__Address
    max_hours         : int                             = 4
    mode              : Enum__S3_Server__Mode           = Enum__S3_Server__Mode.FULL_PROXY
    backend           : Enum__S3_Server__Backend        = Enum__S3_Server__Backend.MEMORY
    aws_region_target : Safe_Str__AWS__Region
