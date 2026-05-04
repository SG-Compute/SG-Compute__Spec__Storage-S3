# ═══════════════════════════════════════════════════════════════════════════════
# SG/Compute Specs — S3 Server: S3_Server__AWS__Client
# Composition shell for per-concern AWS helpers.
#
# Tag convention:
#   sg:section    : s3-server
#   sg:stack-name : {stack_name}
#   sg:allowed-ip : {caller_ip}
#   sg:creator    : git email or $USER
#   sg:mode       : {mode}
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.Type_Safe                                                import Type_Safe

from sgraph_ai_service_playwright__cli.aws.Stack__Naming                            import Stack__Naming


TAG_SECTION_KEY     = 'sg:section'
TAG_SECTION_VALUE   = 's3-server'
TAG_STACK_NAME_KEY  = 'sg:stack-name'
TAG_ALLOWED_IP_KEY  = 'sg:allowed-ip'
TAG_CREATOR_KEY     = 'sg:creator'
TAG_MODE_KEY        = 'sg:mode'


S3_SERVER_NAMING = Stack__Naming(section_prefix='s3srv')


class S3_Server__AWS__Client(Type_Safe):
    sg       : object = None
    ami      : object = None
    instance : object = None
    tags     : object = None
    launch   : object = None

    def setup(self) -> 'S3_Server__AWS__Client':
        from sg_compute_specs.s3_server.service.S3_Server__SG__Helper       import S3_Server__SG__Helper
        from sg_compute_specs.s3_server.service.S3_Server__AMI__Helper      import S3_Server__AMI__Helper
        from sg_compute_specs.s3_server.service.S3_Server__Instance__Helper import S3_Server__Instance__Helper
        from sg_compute_specs.s3_server.service.S3_Server__Launch__Helper   import S3_Server__Launch__Helper
        from sg_compute_specs.s3_server.service.S3_Server__Tags__Builder    import S3_Server__Tags__Builder
        self.sg       = S3_Server__SG__Helper      ()
        self.ami      = S3_Server__AMI__Helper     ()
        self.instance = S3_Server__Instance__Helper()
        self.tags     = S3_Server__Tags__Builder   ()
        self.launch   = S3_Server__Launch__Helper  ()
        return self
