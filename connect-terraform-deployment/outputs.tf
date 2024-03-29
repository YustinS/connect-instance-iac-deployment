# outputs.tf

output "connect_instance_alias" {
  description = "The Alias of the created Connect Instance"
  value       = aws_connect_instance.connect_instance.instance_alias
}

output "connect_instance_arn" {
  description = "The ARN of the created Connect Instance"
  value       = aws_connect_instance.connect_instance.arn
}

output "connect_instance_id" {
  description = "The ID of the created Connect Instance"
  value       = aws_connect_instance.connect_instance.id
}

output "connect_service_role" {
  description = "The Role for the Connect Service Role that is used by Connect to interact with other AWS Services"
  value       = aws_connect_instance.connect_instance.service_role
}

output "connect_instance_storage_bucket" {
  description = "Name of the S3 Bucket (if created) that will store content generated by Connect, otherwise null if using a provided bucket."
  value       = local.create_new_bucket ? aws_s3_bucket.connect_content_bucket[0].id : null
}

output "connect_cloudwatch_log_group_name" {
  description = "The name of the created CloudWatch Log Group the Connect Logs will be written to"
  value       = var.contact_flow_logs_enabled ? aws_cloudwatch_log_group.connect_instance_logs[0].name : null
}
