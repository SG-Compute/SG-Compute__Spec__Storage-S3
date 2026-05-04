# ═══════════════════════════════════════════════════════════════════════════════
# SG/Compute Specs — S3 Server: S3_Server__User_Data__Builder
# cloud-init for AL2023 + Docker CE + S3 server container on port 9000.
# No AWS credentials in user-data — container uses instance IAM role.
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.Type_Safe                                                import Type_Safe


LOG_FILE      = '/var/log/sg-s3-server-boot.log'
S3_IMAGE      = 'sgraph/s3-server:latest'
S3_SERVER_PORT = 9000

BASE_TEMPLATE = """\
#!/usr/bin/env bash
set -euo pipefail
exec > >(tee -a {log_file}) 2>&1
echo "[sg-s3-server] boot starting at $(date -u +%FT%TZ)"

STACK_NAME='{stack_name}'
REGION='{region}'

echo "[sg-s3-server] installing Docker on AL2023..."
dnf install -y docker
systemctl enable --now docker

echo "[sg-s3-server] installing docker compose plugin..."
mkdir -p /usr/local/lib/docker/cli-plugins
curl -fsSL "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64" \\
    -o /usr/local/lib/docker/cli-plugins/docker-compose
chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

echo "[sg-s3-server] verifying docker..."
docker version

systemctl enable --now amazon-ssm-agent || true
"""

SERVER_TEMPLATE = """\
# ── S3 server ────────────────────────────────────────────────────────────────
echo "[sg-s3-server] starting S3 server (port {port})..."

docker run -d \\
  --name sg-s3-server \\
  --restart=unless-stopped \\
  -p {port}:{port} \\
  -e S3_SERVER_MODE="{mode}" \\
  -e S3_SERVER_BACKEND="{backend}" \\
  -e S3_SERVER_AWS_REGION="{aws_region_target}" \\
  {image}

echo "[sg-s3-server] S3 server started"
"""

FOOTER_TEMPLATE = """\
{shutdown_line}

echo "[sg-s3-server] boot complete at $(date -u +%FT%TZ)"
"""

SHUTDOWN_TEMPLATE = 'shutdown -h +{minutes}  # auto-terminate after {hours}h'
SHUTDOWN_DISABLED = '# max_hours=0 — no auto-terminate'

PLACEHOLDERS = ('stack_name', 'region', 'log_file', 'mode', 'backend', 'aws_region_target', 'shutdown_line')


class S3_Server__User_Data__Builder(Type_Safe):

    def render(self, stack_name      : str ,
                     region          : str ,
                     mode            : str = 'full-proxy',
                     backend         : str = 'memory'    ,
                     aws_region_target: str = ''         ,
                     max_hours       : int = 4           ) -> str:
        shutdown_line = (SHUTDOWN_TEMPLATE.format(minutes=max_hours * 60, hours=max_hours)
                         if max_hours > 0 else SHUTDOWN_DISABLED)
        script = BASE_TEMPLATE.format(stack_name=str(stack_name),
                                      region    =str(region)    ,
                                      log_file  =LOG_FILE       )
        script += SERVER_TEMPLATE.format(port             = S3_SERVER_PORT          ,
                                         mode             = str(mode)               ,
                                         backend          = str(backend)            ,
                                         aws_region_target= str(aws_region_target)  ,
                                         image            = S3_IMAGE                )
        script += FOOTER_TEMPLATE.format(shutdown_line=shutdown_line)
        return script
