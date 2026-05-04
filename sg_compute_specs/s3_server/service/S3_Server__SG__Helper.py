# ═══════════════════════════════════════════════════════════════════════════════
# SG/Compute Specs — S3 Server: S3_Server__SG__Helper
# Per-node security group: TCP 9000 (S3 API + call-log UI), TCP 22 (debug).
# GroupName never starts with "sg-" (AWS reserved prefix).
# ═══════════════════════════════════════════════════════════════════════════════

import boto3                                                                        # EXCEPTION — narrow boto3 boundary

from osbot_utils.type_safe.Type_Safe                                                import Type_Safe

from sg_compute_specs.s3_server.primitives.Safe_Str__IP__Address                   import Safe_Str__IP__Address
from sg_compute_specs.s3_server.primitives.Safe_Str__S3_Server__Stack__Name        import Safe_Str__S3_Server__Stack__Name
from sg_compute_specs.s3_server.service.S3_Server__AWS__Client                     import S3_SERVER_NAMING, TAG_SECTION_KEY, TAG_SECTION_VALUE


S3_SERVER_PORT = 9000


class S3_Server__SG__Helper(Type_Safe):

    def ec2_client(self, region: str):
        return boto3.client('ec2', region_name=region)

    def ensure_security_group(self, region     : str                               ,
                                     stack_name : Safe_Str__S3_Server__Stack__Name ,
                                     caller_ip  : Safe_Str__IP__Address            ) -> str:
        ec2     = self.ec2_client(region)
        sg_name = S3_SERVER_NAMING.sg_name_for_stack(stack_name)
        cidr    = f'{str(caller_ip)}/32'

        existing = ec2.describe_security_groups(
            Filters=[{'Name': 'group-name', 'Values': [sg_name]}]).get('SecurityGroups', [])

        if existing:
            sg_id = existing[0].get('GroupId', '')
        else:
            created = ec2.create_security_group(
                GroupName         = sg_name                                               ,
                Description       = f'SG S3 server node: {str(stack_name)}'              ,
                TagSpecifications = [{'ResourceType': 'security-group',
                                      'Tags': [{'Key': TAG_SECTION_KEY, 'Value': TAG_SECTION_VALUE}]}])
            sg_id = created.get('GroupId', '')

        for port in [S3_SERVER_PORT, 22]:
            try:
                ec2.authorize_security_group_ingress(
                    GroupId       = sg_id,
                    IpPermissions = [{'IpProtocol': 'tcp'                                                   ,
                                      'FromPort'  : port                                                    ,
                                      'ToPort'    : port                                                    ,
                                      'IpRanges'  : [{'CidrIp': cidr, 'Description': f's3srv caller /32 port {port}'}]}])
            except Exception as exc:
                if 'InvalidPermission.Duplicate' not in str(exc):
                    raise
        return sg_id

    def delete_security_group(self, region: str, security_group_id: str) -> bool:
        try:
            self.ec2_client(region).delete_security_group(GroupId=security_group_id)
            return True
        except Exception:
            return False
