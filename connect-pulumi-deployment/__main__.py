"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws

# Configs required
config = pulumi.Config()
name_prefix = config.require("namePrefix")
environment = config.require("environment")
enable_contact_lens = config.get_bool(key="enableContactLens", default=False)

instance_alias = f"{name_prefix}-connect-{environment}"
bucket_name = f"{name_prefix}-connect-content-bucket-{environment}"

# Resources from here

# S3 Content
connect_storage_bucket = aws.s3.BucketV2(
    "ConnectStorageBucket",
    bucket=bucket_name,
    force_destroy=True,
)

connect_bucket_ownership_controls = aws.s3.BucketOwnershipControls(
    "ConnectContentBucket",
    bucket=connect_storage_bucket.id,
    rule=aws.s3.BucketOwnershipControlsRuleArgs(
        object_ownership="ObjectWriter",
    ),
)

connect_bucket_acl = aws.s3.BucketAclV2(
    "ConnectBucketACL",
    bucket=connect_storage_bucket.id,
    acl="private",
    opts=pulumi.ResourceOptions(depends_on=[connect_bucket_ownership_controls]),
)

connect_bucket_encryption = aws.s3.BucketServerSideEncryptionConfigurationV2(
    "ConnectBucketEncryption",
    bucket=connect_storage_bucket.id,
    rules=[
        aws.s3.BucketServerSideEncryptionConfigurationV2RuleArgs(
            bucket_key_enabled=True,
            apply_server_side_encryption_by_default=aws.s3.BucketServerSideEncryptionConfigurationV2RuleApplyServerSideEncryptionByDefaultArgs(
                # kms_master_key_id=mykey.arn,
                sse_algorithm="AES256",
            ),
        )
    ],
)

connect_bucket_public_access_block = aws.s3.BucketPublicAccessBlock(
    "ConnectBucketPublicAccessBlock",
    bucket=connect_storage_bucket.id,
    block_public_acls=True,
    block_public_policy=True,
    ignore_public_acls=True,
    restrict_public_buckets=True,
)

# Connect Content
connect_log_group = aws.cloudwatch.LogGroup(
    "ConnectLogGroup",
    name=f"/aws/connect/{instance_alias}",
    retention_in_days=731,
)

connect_instance = aws.connect.Instance(
    "ConnectInstance",
    auto_resolve_best_voices_enabled=True,
    contact_flow_logs_enabled=True,
    contact_lens_enabled=enable_contact_lens,
    early_media_enabled=True,
    identity_management_type="CONNECT_MANAGED",
    inbound_calls_enabled=True,
    instance_alias=instance_alias,
    multi_party_conference_enabled=True,
    outbound_calls_enabled=True,
)

transcript_storage = aws.connect.InstanceStorageConfig(
    "TranscriptRecordingStorage",
    instance_id=connect_instance.id,
    resource_type="CHAT_TRANSCRIPTS",
    storage_config=aws.connect.InstanceStorageConfigStorageConfigArgs(
        s3_config=aws.connect.InstanceStorageConfigStorageConfigS3ConfigArgs(
            bucket_name=connect_storage_bucket.id,
            bucket_prefix=f"connect/{instance_alias}/ChatTranscripts",
            # encryption_config=aws.connect.InstanceStorageConfigStorageConfigS3ConfigEncryptionConfigArgs(
            #     encryption_type="KMS",
            #     key_id=aws_kms_key["example"]["arn"],
            # ),
        ),
        storage_type="S3",
    ),
)

transcript_storage = aws.connect.InstanceStorageConfig(
    "RecordingStorage",
    instance_id=connect_instance.id,
    resource_type="CALL_RECORDINGS",
    storage_config=aws.connect.InstanceStorageConfigStorageConfigArgs(
        s3_config=aws.connect.InstanceStorageConfigStorageConfigS3ConfigArgs(
            bucket_name=connect_storage_bucket.id,
            bucket_prefix=f"connect/{instance_alias}/CallRecordings",
            # encryption_config=aws.connect.InstanceStorageConfigStorageConfigS3ConfigEncryptionConfigArgs(
            #     encryption_type="KMS",
            #     key_id=aws_kms_key["example"]["arn"],
            # ),
        ),
        storage_type="S3",
    ),
)

transcript_storage = aws.connect.InstanceStorageConfig(
    "ReportStorageConfig",
    instance_id=connect_instance.id,
    resource_type="SCHEDULED_REPORTS",
    storage_config=aws.connect.InstanceStorageConfigStorageConfigArgs(
        s3_config=aws.connect.InstanceStorageConfigStorageConfigS3ConfigArgs(
            bucket_name=connect_storage_bucket.id,
            bucket_prefix=f"connect/{instance_alias}/Reports",
            # encryption_config=aws.connect.InstanceStorageConfigStorageConfigS3ConfigEncryptionConfigArgs(
            #     encryption_type="KMS",
            #     key_id=aws_kms_key["example"]["arn"],
            # ),
        ),
        storage_type="S3",
    ),
)

pulumi.export("Connect Instance ARN", connect_instance.arn)
pulumi.export("Connect Instance ID", connect_instance.id)
pulumi.export("Connect Log Group Name", connect_log_group.name)
pulumi.export("Connect S3 Bucket", connect_storage_bucket.id)
