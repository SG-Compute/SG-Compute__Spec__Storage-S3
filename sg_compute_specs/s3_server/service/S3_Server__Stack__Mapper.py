# ═══════════════════════════════════════════════════════════════════════════════
# SG/Compute Specs — S3 Server: S3_Server__Stack__Mapper
# Pure mapper: boto3 instance dict → Schema__S3_Server__Info.
# Builds s3_endpoint_url, call_log_url, and ui_url from public_ip.
# ═══════════════════════════════════════════════════════════════════════════════

import time

from osbot_utils.type_safe.Type_Safe                                                import Type_Safe

from sg_compute_specs.s3_server.enums.Enum__S3_Server__Backend                     import Enum__S3_Server__Backend
from sg_compute_specs.s3_server.enums.Enum__S3_Server__Mode                        import Enum__S3_Server__Mode
from sg_compute_specs.s3_server.enums.Enum__S3_Server__Stack__State                import Enum__S3_Server__Stack__State
from sg_compute_specs.s3_server.schemas.Schema__S3_Server__Info                    import Schema__S3_Server__Info
from sg_compute_specs.s3_server.service.S3_Server__AWS__Client                     import TAG_ALLOWED_IP_KEY, TAG_MODE_KEY, TAG_STACK_NAME_KEY

S3_SERVER_PORT = 9000


def _tag(details: dict, key: str) -> str:
    for tag in details.get('Tags', []):
        if tag.get('Key') == key:
            return tag.get('Value', '')
    return ''


def _state_str(details: dict) -> str:
    state_raw = details.get('State', {})
    return state_raw.get('Name', '') if isinstance(state_raw, dict) else str(state_raw)


def _state_to_enum(state_str: str) -> Enum__S3_Server__Stack__State:
    mapping = {'pending'      : Enum__S3_Server__Stack__State.PENDING    ,
               'running'      : Enum__S3_Server__Stack__State.READY      ,
               'shutting-down': Enum__S3_Server__Stack__State.TERMINATING,
               'terminated'   : Enum__S3_Server__Stack__State.TERMINATED }
    return mapping.get(state_str, Enum__S3_Server__Stack__State.UNKNOWN)


def _mode_from_tag(tag_value: str) -> Enum__S3_Server__Mode:
    for m in Enum__S3_Server__Mode:
        if m.value == tag_value:
            return m
    return Enum__S3_Server__Mode.FULL_PROXY


def _uptime_seconds(details: dict) -> int:
    launch_time = details.get('LaunchTime')
    if not launch_time:
        return 0
    try:
        import datetime
        if hasattr(launch_time, 'timestamp'):
            return int(time.time() - launch_time.timestamp())
        dt = datetime.datetime.fromisoformat(str(launch_time).replace('Z', '+00:00'))
        return int(time.time() - dt.timestamp())
    except Exception:
        return 0


class S3_Server__Stack__Mapper(Type_Safe):

    def to_info(self, details: dict, region: str) -> Schema__S3_Server__Info:
        public_ip = details.get('PublicIpAddress', '') or ''
        mode      = _mode_from_tag(_tag(details, TAG_MODE_KEY))
        return Schema__S3_Server__Info(
            stack_name        = _tag(details, TAG_STACK_NAME_KEY)                                      ,
            aws_name_tag      = _tag(details, 'Name')                                                  ,
            instance_id       = details.get('InstanceId', '')                                          ,
            region            = region                                                                  ,
            ami_id            = details.get('ImageId', '')                                             ,
            instance_type     = details.get('InstanceType', '')                                        ,
            security_group_id = (details.get('SecurityGroups', [{}])[0].get('GroupId', '')
                                 if details.get('SecurityGroups') else '')                              ,
            allowed_ip        = _tag(details, TAG_ALLOWED_IP_KEY)                                      ,
            public_ip         = public_ip                                                               ,
            state             = _state_to_enum(_state_str(details))                                    ,
            mode              = mode                                                                    ,
            s3_endpoint_url   = f'http://{public_ip}:{S3_SERVER_PORT}'  if public_ip else ''          ,
            call_log_url      = f'http://{public_ip}:{S3_SERVER_PORT}/call-log' if public_ip else ''  ,
            ui_url            = f'http://{public_ip}:{S3_SERVER_PORT}/ui/'      if public_ip else ''  ,
            launch_time       = str(details.get('LaunchTime', ''))                                     ,
            uptime_seconds    = _uptime_seconds(details)                                               )
