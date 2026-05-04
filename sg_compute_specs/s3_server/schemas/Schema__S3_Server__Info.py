# ═══════════════════════════════════════════════════════════════════════════════
# SG/Compute Specs — S3 Server: Schema__S3_Server__Info
# Public view of one S3 server EC2 node. Pure data.
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text        import Safe_Str__Text

from sgraph_ai_service_playwright__cli.ec2.primitives.Safe_Str__AMI__Id             import Safe_Str__AMI__Id
from sgraph_ai_service_playwright__cli.ec2.primitives.Safe_Str__Instance__Id        import Safe_Str__Instance__Id
from sgraph_ai_service_playwright__cli.observability.primitives.Safe_Str__AWS__Region import Safe_Str__AWS__Region

from sg_compute_specs.s3_server.enums.Enum__S3_Server__Backend                     import Enum__S3_Server__Backend
from sg_compute_specs.s3_server.enums.Enum__S3_Server__Mode                        import Enum__S3_Server__Mode
from sg_compute_specs.s3_server.enums.Enum__S3_Server__Stack__State                import Enum__S3_Server__Stack__State
from sg_compute_specs.s3_server.primitives.Safe_Str__IP__Address                   import Safe_Str__IP__Address
from sg_compute_specs.s3_server.primitives.Safe_Str__S3_Server__Stack__Name        import Safe_Str__S3_Server__Stack__Name


class Schema__S3_Server__Info(Type_Safe):
    stack_name        : Safe_Str__S3_Server__Stack__Name
    aws_name_tag      : Safe_Str__Text
    instance_id       : Safe_Str__Instance__Id
    region            : Safe_Str__AWS__Region
    ami_id            : Safe_Str__AMI__Id
    instance_type     : Safe_Str__Text
    security_group_id : Safe_Str__Text
    allowed_ip        : Safe_Str__IP__Address
    public_ip         : Safe_Str__Text
    state             : Enum__S3_Server__Stack__State   = Enum__S3_Server__Stack__State.UNKNOWN
    mode              : Enum__S3_Server__Mode           = Enum__S3_Server__Mode.FULL_PROXY
    backend           : Enum__S3_Server__Backend        = Enum__S3_Server__Backend.MEMORY
    s3_endpoint_url   : Safe_Str__Text
    call_log_url      : Safe_Str__Text
    ui_url            : Safe_Str__Text
    launch_time       : Safe_Str__Text
    uptime_seconds    : int  = 0
    spot              : bool = False
