# ═══════════════════════════════════════════════════════════════════════════════
# sg_s3_server — S3__XML__Response
# Well-formed AWS XML responses for all Phase 1 operations.
# boto3 and all S3 SDKs parse these without modification.
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.Type_Safe                                                import Type_Safe


class S3__XML__Response(Type_Safe):

    def list_buckets(self, buckets: list, owner_id: str = 'sg-server', owner_name: str = 'sg-server') -> str:
        items = ''.join(f'<Bucket><Name>{b["Name"]}</Name><CreationDate>1970-01-01T00:00:00.000Z</CreationDate></Bucket>'
                        for b in buckets)
        return (f'<?xml version="1.0" encoding="UTF-8"?>'
                f'<ListAllMyBucketsResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">'
                f'<Owner><ID>{owner_id}</ID><DisplayName>{owner_name}</DisplayName></Owner>'
                f'<Buckets>{items}</Buckets>'
                f'</ListAllMyBucketsResult>')

    def list_objects_v2(self, bucket: str, objects: list, prefix: str = '',
                        max_keys: int = 1000, truncated: bool = False) -> str:
        items = ''.join(
            f'<Contents>'
            f'<Key>{o["Key"]}</Key>'
            f'<Size>{o["Size"]}</Size>'
            f'<LastModified>{o.get("LastModified", "")}</LastModified>'
            f'<ETag>&quot;{o.get("ETag", "")}&quot;</ETag>'
            f'<StorageClass>STANDARD</StorageClass>'
            f'</Contents>'
            for o in objects)
        return (f'<?xml version="1.0" encoding="UTF-8"?>'
                f'<ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">'
                f'<Name>{bucket}</Name>'
                f'<Prefix>{prefix}</Prefix>'
                f'<MaxKeys>{max_keys}</MaxKeys>'
                f'<KeyCount>{len(objects)}</KeyCount>'
                f'<IsTruncated>{"true" if truncated else "false"}</IsTruncated>'
                f'{items}'
                f'</ListBucketResult>')

    def create_bucket(self, bucket: str, location: str = '/') -> str:
        return (f'<?xml version="1.0" encoding="UTF-8"?>'
                f'<CreateBucketConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">'
                f'<LocationConstraint>{location}</LocationConstraint>'
                f'</CreateBucketConfiguration>')

    def sts_get_caller_identity(self, account: str = '000000000000',
                                 user_id: str = 'AROASG000000000000000',
                                 arn: str = 'arn:aws:iam::000000000000:user/sg-server') -> str:
        return (f'<?xml version="1.0" encoding="UTF-8"?>'
                f'<GetCallerIdentityResponse xmlns="https://sts.amazonaws.com/doc/2011-06-15/">'
                f'<GetCallerIdentityResult>'
                f'<Account>{account}</Account>'
                f'<UserId>{user_id}</UserId>'
                f'<Arn>{arn}</Arn>'
                f'</GetCallerIdentityResult>'
                f'<ResponseMetadata>'
                f'<RequestId>sg-synthetic-sts-response</RequestId>'
                f'</ResponseMetadata>'
                f'</GetCallerIdentityResponse>')
