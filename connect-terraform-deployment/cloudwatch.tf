# cloudwatch.tf

resource "aws_cloudwatch_log_group" "connect_instance_logs" {
  count = var.contact_flow_logs_enabled ? 1 : 0

  name              = "/aws/connect/${local.instance_name}"
  tags              = var.tags
  retention_in_days = var.log_retention_days
  kms_key_id        = var.log_encryption_cmk != null ? var.log_encryption_cmk : null
}
