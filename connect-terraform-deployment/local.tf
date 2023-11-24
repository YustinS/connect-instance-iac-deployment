# locals.tf

locals {
  instance_name   = "${var.name_prefix}-connect-${var.environment}"
  s3_connect_name = lower("${var.name_prefix}-connect-content-bucket-${var.environment}")

  create_new_bucket      = var.existing_s3_bucket_name == null ? true : false
  s3_storage_bucket_name = var.existing_s3_bucket_name != null ? var.existing_s3_bucket_name : aws_s3_bucket.connect_content_bucket[0].id
}
