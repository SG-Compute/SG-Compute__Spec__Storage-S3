# ═══════════════════════════════════════════════════════════════════════════════
# SG/Compute Specs — S3 Server: Schema__S3_Server__List
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.Type_Safe                                                import Type_Safe

from sgraph_ai_service_playwright__cli.observability.primitives.Safe_Str__AWS__Region import Safe_Str__AWS__Region

from sg_compute_specs.s3_server.collections.List__Schema__S3_Server__Info          import List__Schema__S3_Server__Info


class Schema__S3_Server__List(Type_Safe):
    region : Safe_Str__AWS__Region
    stacks : List__Schema__S3_Server__Info
    total  : int = 0
