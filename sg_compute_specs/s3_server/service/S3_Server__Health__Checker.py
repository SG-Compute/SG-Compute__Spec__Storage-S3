# ═══════════════════════════════════════════════════════════════════════════════
# SG/Compute Specs — S3 Server: S3_Server__Health__Checker
# Polls GET http://{public_ip}:9000/health until {"status":"ok"} or timeout.
# ═══════════════════════════════════════════════════════════════════════════════

import time

import requests

from osbot_utils.type_safe.Type_Safe                                                import Type_Safe

from sg_compute_specs.s3_server.enums.Enum__S3_Server__Stack__State                import Enum__S3_Server__Stack__State
from sg_compute_specs.s3_server.schemas.Schema__S3_Server__Health__Response        import Schema__S3_Server__Health__Response

S3_SERVER_PORT = 9000


class S3_Server__Health__Checker(Type_Safe):
    instance : object = None                                                        # S3_Server__Instance__Helper (injected)

    def check(self, region: str, stack_name: str,
              timeout_sec: int = 300, poll_sec: int = 10) -> Schema__S3_Server__Health__Response:
        deadline = time.monotonic() + timeout_sec
        t0       = time.monotonic()

        while time.monotonic() < deadline or timeout_sec == 0:
            details = self.instance.find_by_stack_name(region, stack_name)
            if details is None:
                return Schema__S3_Server__Health__Response(
                    stack_name = stack_name       ,
                    message    = 'stack not found',
                    elapsed_ms = int((time.monotonic()-t0)*1000))

            public_ip  = details.get('PublicIpAddress', '') or ''
            state_name = (details.get('State') or {}).get('Name', '')

            if state_name in ('shutting-down', 'terminated'):
                return Schema__S3_Server__Health__Response(
                    stack_name = stack_name                               ,
                    state      = Enum__S3_Server__Stack__State.TERMINATED ,
                    message    = f'instance is {state_name}'             ,
                    elapsed_ms = int((time.monotonic()-t0)*1000)         )

            if state_name == 'running' and public_ip:
                try:
                    resp = requests.get(f'http://{public_ip}:{S3_SERVER_PORT}/health', timeout=5)
                    if resp.status_code == 200 and resp.json().get('status') == 'ok':
                        return Schema__S3_Server__Health__Response(
                            stack_name = stack_name                             ,
                            state      = Enum__S3_Server__Stack__State.READY   ,
                            healthy    = True                                   ,
                            message    = 'S3 server ready'                     ,
                            elapsed_ms = int((time.monotonic()-t0)*1000)       )
                except Exception:
                    pass

            if timeout_sec == 0:
                break
            time.sleep(poll_sec)

        return Schema__S3_Server__Health__Response(
            stack_name = stack_name                                            ,
            state      = Enum__S3_Server__Stack__State.UNKNOWN                ,
            message    = f'timed out after {timeout_sec}s'                    ,
            elapsed_ms = int((time.monotonic()-t0)*1000)                      )
