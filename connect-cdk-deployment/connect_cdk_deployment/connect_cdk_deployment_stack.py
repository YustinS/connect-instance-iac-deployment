from aws_cdk import (
    Stack,
    # NestedStack,
    CfnParameter,
    Duration,
    RemovalPolicy,
    aws_connect as connect,
    aws_logs as logs,
    aws_s3 as s3,
)
from constructs import Construct


class ConnectCdkDeploymentStack(Stack):
    """
    Primary stack configuration. This is where the primary components are deployed from
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Parameters required for creation can go here
        name_prefix = CfnParameter(
            self,
            "namePrefix",
            type="String",
            description="Prefix used to make names distinct across the deployment",
            allowed_pattern="[a-z0-9-]+",
            constraint_description="Only alphanumeric values (a-z case sensitive and 0-9) are allowed in this parameter",
        )

        environment = CfnParameter(
            self,
            "environment",
            type="String",
            description="The lifecycle of the enviroment, such as poc, dev, test, and so forth. This is added as a suffix to resources",
            allowed_pattern="[a-z]+",
            constraint_description="Only lowercase letters are allowed in this parameter",
        )

        enable_contact_lens = CfnParameter(
            self,
            "enableContactLens",
            type="String",
            allowed_values=["true", "false"],
            description="Should Contact Lens be enabled for the Instance.",
            default="false",
        )

        # Short evaulation of Boolean
        enable_contact_lens_bool = enable_contact_lens.value_as_string == "true"

        instance_alias = (
            f"{name_prefix.value_as_string}-connect-{environment.value_as_string}"
        )
        bucket_name = f"{name_prefix.value_as_string}-connect-content-bucket-{environment.value_as_string}"

        connect_log_group = logs.LogGroup(
            self,
            "ConnectLogGroup",
            log_group_name=f"/aws/connect/{instance_alias}",
            retention=logs.RetentionDays.TWO_YEARS,
            # Apply the policy so a deletion doesn't orphan the resource. In production this likely would be left
            # for long term retention purposes.
            removal_policy=RemovalPolicy.DESTROY,
        )

        connect_instance = connect.CfnInstance(
            self,  # type: ignore
            "ConnectInstance",
            attributes=connect.CfnInstance.AttributesProperty(
                inbound_calls=True,
                outbound_calls=True,
                # the properties below are optional
                auto_resolve_best_voices=True,
                contactflow_logs=True,
                contact_lens=enable_contact_lens_bool,
                early_media=True,
            ),
            identity_management_type="CONNECT_MANAGED",
            instance_alias=instance_alias,  # Required if identity_management_type is not "EXISTING_DIRECTORY"
        )

        # Apply the policy so a deletion doesn't orphan the resource
        connect_instance.apply_removal_policy(
            policy=RemovalPolicy.DESTROY,
        )

        connect_storage_tiering = s3.IntelligentTieringConfiguration(
            name="ArchiveOlderData",
            archive_access_tier_time=Duration.days(730),
        )

        connect_storage_bucket = s3.Bucket(
            self,
            "ConnectStorageBucket",
            bucket_name=bucket_name,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            # encryption_key="",
            enforce_ssl=True,
            intelligent_tiering_configurations=[connect_storage_tiering],
            object_ownership=s3.ObjectOwnership.BUCKET_OWNER_ENFORCED,
            # Apply the policy so a deletion doesn't orphan the resource. In production this likely would be left
            # for long term retention purposes.
            removal_policy=RemovalPolicy.DESTROY,
        )

        _ = connect.CfnInstanceStorageConfig(
            self,
            "TranscriptStorageConfig",
            instance_arn=connect_instance.attr_arn,
            resource_type="CHAT_TRANSCRIPTS",
            storage_type="S3",
            s3_config=connect.CfnInstanceStorageConfig.S3ConfigProperty(
                bucket_name=connect_storage_bucket.bucket_name,
                bucket_prefix=f"connect/{instance_alias}/ChatTranscripts",
                # the properties below are optional
                # encryption_config=connect.CfnInstanceStorageConfig.EncryptionConfigProperty(
                #    encryption_type="KMS", key_id=""
                # ),
            ),
        )

        _ = connect.CfnInstanceStorageConfig(
            self,
            "RecordingStorageConfig",
            instance_arn=connect_instance.attr_arn,
            resource_type="CALL_RECORDINGS",
            storage_type="S3",
            s3_config=connect.CfnInstanceStorageConfig.S3ConfigProperty(
                bucket_name=connect_storage_bucket.bucket_name,
                bucket_prefix=f"connect/{instance_alias}/CallRecordings",
                # the properties below are optional
                # encryption_config=connect.CfnInstanceStorageConfig.EncryptionConfigProperty(
                #    encryption_type="KMS", key_id=""
                # ),
            ),
        )

        _ = connect.CfnInstanceStorageConfig(
            self,
            "ReportStorageConfig",
            instance_arn=connect_instance.attr_arn,
            resource_type="SCHEDULED_REPORTS",
            storage_type="S3",
            s3_config=connect.CfnInstanceStorageConfig.S3ConfigProperty(
                bucket_name=connect_storage_bucket.bucket_name,
                bucket_prefix=f"connect/{instance_alias}/Reports",
                # the properties below are optional
                # encryption_config=connect.CfnInstanceStorageConfig.EncryptionConfigProperty(
                #    encryption_type="KMS", key_id=""
                # ),
            ),
        )

        self.connect_instance_arn = connect_instance.attr_arn
        self.connect_instance_id = connect_instance.attr_id
        self.connect_log_group_name = connect_log_group.log_group_name
        self.connect_s3_bucket = connect_storage_bucket.bucket_name


# class ConnectInstance(NestedStack):
#     """
#     Contains the core Connect components. These are deployed
#     irrespective of the other settings
#     """

#     def __init__(
#         self,
#         scope: Construct,
#         construct_id: str,
#         instance_alias: str,
#         contact_lens_enabled: bool,
#         **kwargs,
#     ) -> None:
#         super().__init__(scope, construct_id, **kwargs)
