# ═══════════════════════════════════════════════════════════════════════════════
# SG/Compute Specs — S3 Server: S3_Server__Tags__Builder
# Builds EC2 tag list for an S3 server node. Pure mapper — no AWS calls.
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                         import List

from osbot_utils.type_safe.Type_Safe                                                import Type_Safe

from sg_compute_specs.s3_server.enums.Enum__S3_Server__Mode                        import Enum__S3_Server__Mode
from sg_compute_specs.s3_server.primitives.Safe_Str__IP__Address                   import Safe_Str__IP__Address
from sg_compute_specs.s3_server.primitives.Safe_Str__S3_Server__Stack__Name        import Safe_Str__S3_Server__Stack__Name
from sg_compute_specs.s3_server.service.S3_Server__AWS__Client                     import (S3_SERVER_NAMING   ,
                                                                                              TAG_ALLOWED_IP_KEY ,
                                                                                              TAG_CREATOR_KEY    ,
                                                                                              TAG_MODE_KEY       ,
                                                                                              TAG_SECTION_KEY    ,
                                                                                              TAG_SECTION_VALUE  ,
                                                                                              TAG_STACK_NAME_KEY )


class S3_Server__Tags__Builder(Type_Safe):

    def build(self, stack_name : Safe_Str__S3_Server__Stack__Name ,
                    caller_ip  : Safe_Str__IP__Address             ,
                    mode       : Enum__S3_Server__Mode             = Enum__S3_Server__Mode.FULL_PROXY,
                    creator    : str                               = '') -> List[dict]:
        return [{'Key': 'Name'             , 'Value': S3_SERVER_NAMING.aws_name_for_stack(stack_name)},
                {'Key': TAG_SECTION_KEY    , 'Value': TAG_SECTION_VALUE                              },
                {'Key': TAG_STACK_NAME_KEY , 'Value': str(stack_name)                                },
                {'Key': TAG_ALLOWED_IP_KEY , 'Value': str(caller_ip)                                 },
                {'Key': TAG_MODE_KEY       , 'Value': str(mode.value)                                },
                {'Key': TAG_CREATOR_KEY    , 'Value': str(creator) or 'unknown'                      }]
