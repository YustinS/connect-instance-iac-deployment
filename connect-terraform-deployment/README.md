# Amazon Connect Base Instance Terraform Module

Terraform module to create a basic instance of Amazon Connect for further usage. This should then be extended further with extra functionality to suit your needs, such as chaining together other modules or creating other Terraform resources to achieve the desired outcome.

Importantly, if you are creating a Connect Instance using the `EXISTING_DIRECTORY` or `SAML` in the variable `connect_identity_management_type` then you will need to create the directory or SAML provider first. This module will not create these for you, as these may be reused resources rather than completely new.

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.1.0 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | >= 5.0.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 5.10.0 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_cloudwatch_log_group.connect_instance_logs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_group) | resource |
| [aws_connect_instance.connect_instance](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/connect_instance) | resource |
| [aws_connect_instance_storage_config.call_recordings](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/connect_instance_storage_config) | resource |
| [aws_connect_instance_storage_config.chat_transcripts](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/connect_instance_storage_config) | resource |
| [aws_connect_instance_storage_config.scheduled_reports](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/connect_instance_storage_config) | resource |
| [aws_s3_bucket.connect_content_bucket](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket) | resource |
| [aws_s3_bucket_acl.content_bucket](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_acl) | resource |
| [aws_s3_bucket_ownership_controls.content_bucket](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_ownership_controls) | resource |
| [aws_s3_bucket_public_access_block.content_bucket](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_public_access_block) | resource |
| [aws_s3_bucket_server_side_encryption_configuration.content_bucket](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_server_side_encryption_configuration) | resource |
| [aws_s3_bucket_versioning.content_bucket](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_versioning) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_auto_resolve_best_voices_enabled"></a> [auto\_resolve\_best\_voices\_enabled](#input\_auto\_resolve\_best\_voices\_enabled) | Will Connect attempt to use the best avilaible voice. Recommended left on unless specific reasons are identified | `bool` | `true` | no |
| <a name="input_connect_existing_directory_id"></a> [connect\_existing\_directory\_id](#input\_connect\_existing\_directory\_id) | If variable `connect_identity_management_type` is set to 'EXISTING\_DIRECTORY', then the ID of the Existing Directory Connect will be joined to | `string` | `"N/A"` | no |
| <a name="input_connect_identity_management_type"></a> [connect\_identity\_management\_type](#input\_connect\_identity\_management\_type) | What Identity Management that Connect will use. Valid values are 'SAML', 'CONNECT\_MANAGED', or 'EXISTING\_DIRECTORY'. 'SAML' or 'EXISTING\_DIRECTORY' will require more resources to be created/managed externally to this module. See https://docs.aws.amazon.com/connect/latest/adminguide/connect-identity-management.html for more information | `string` | n/a | yes |
| <a name="input_contact_flow_logs_enabled"></a> [contact\_flow\_logs\_enabled](#input\_contact\_flow\_logs\_enabled) | Will Connect log Contact Flow activity to CloudWatch logs (if the appropriate setting is enabled in the Contact Flow). Recommended left on to assist with trouble shooting, and disabling logging in specific flows as required | `bool` | `true` | no |
| <a name="input_contact_lens_enabled"></a> [contact\_lens\_enabled](#input\_contact\_lens\_enabled) | Will Connect use Amazon Connect Contact Lens to analyse calls. For proper usage ensure instance storage configuration has been configured, and the appropriate flow blocks configure the usage inside of a contact flow | `bool` | `true` | no |
| <a name="input_early_media_enabled"></a> [early\_media\_enabled](#input\_early\_media\_enabled) | Will Early Media be heard by the Agent when a call is answered. Recommended left on unless specific reasons are identified | `bool` | `true` | no |
| <a name="input_environment"></a> [environment](#input\_environment) | The environment this is running against, such as 'dev', 'test' etc. Will the postfixed to names for consistency. | `string` | n/a | yes |
| <a name="input_existing_s3_bucket_name"></a> [existing\_s3\_bucket\_name](#input\_existing\_s3\_bucket\_name) | If desired an existing S3 Bucket can be used to store content generated by Connect. If not provided, a new S3 Bucket will be created. The prefix for the bucket will be 'connect/{instance\_name}/{content\_prefix}' | `string` | `null` | no |
| <a name="input_inbound_calls_enabled"></a> [inbound\_calls\_enabled](#input\_inbound\_calls\_enabled) | Will the created Connect Instance be able to receive inbound calls | `bool` | `true` | no |
| <a name="input_log_encryption_cmk"></a> [log\_encryption\_cmk](#input\_log\_encryption\_cmk) | KMS ARN for a key used to encrypt created CloudWatch Log Group(s). Ensure KMS has the appropriate Key Policy | `string` | `null` | no |
| <a name="input_log_retention_days"></a> [log\_retention\_days](#input\_log\_retention\_days) | The length of time to maintain logs for | `number` | `90` | no |
| <a name="input_multi_party_conference_enabled"></a> [multi\_party\_conference\_enabled](#input\_multi\_party\_conference\_enabled) | Will Multiparty conferencing be enabled for usage in the instance. For more information see https://docs.aws.amazon.com/connect/latest/adminguide/multi-party-calls.html | `bool` | `false` | no |
| <a name="input_name_prefix"></a> [name\_prefix](#input\_name\_prefix) | String that will be prepended to names for consistency. Contents only [a-zA-Z0-9-] | `string` | n/a | yes |
| <a name="input_outbound_calls_enabled"></a> [outbound\_calls\_enabled](#input\_outbound\_calls\_enabled) | Will the created Connect Instance be able to make outbound calls | `bool` | `true` | no |
| <a name="input_s3_encryption_cmk"></a> [s3\_encryption\_cmk](#input\_s3\_encryption\_cmk) | KMS ARN for a key used to encrypt created S3 Content created from Connect. Ensure KMS has the appropriate key policy, and that Connect or its Service Role has appropriate permissions to encrypt content | `string` | `null` | no |
| <a name="input_tags"></a> [tags](#input\_tags) | A map of tags to assign to resources. These will be specific tags for this module, otherwise it is recommended to use `default_tags` in the AWS Provider | `map(any)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_connect_cloudwatch_log_group_name"></a> [connect\_cloudwatch\_log\_group\_name](#output\_connect\_cloudwatch\_log\_group\_name) | The name of the created CloudWatch Log Group the Connect Logs will be written to |
| <a name="output_connect_instance_alias"></a> [connect\_instance\_alias](#output\_connect\_instance\_alias) | The Alias of the created Connect Instance |
| <a name="output_connect_instance_arn"></a> [connect\_instance\_arn](#output\_connect\_instance\_arn) | The ARN of the created Connect Instance |
| <a name="output_connect_instance_id"></a> [connect\_instance\_id](#output\_connect\_instance\_id) | The ID of the created Connect Instance |
| <a name="output_connect_instance_storage_bucket"></a> [connect\_instance\_storage\_bucket](#output\_connect\_instance\_storage\_bucket) | Name of the S3 Bucket (if created) that will store content generated by Connect, otherwise null if using a provided bucket. |
| <a name="output_connect_service_role"></a> [connect\_service\_role](#output\_connect\_service\_role) | The Role for the Connect Service Role that is used by Connect to interact with other AWS Services |
<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
