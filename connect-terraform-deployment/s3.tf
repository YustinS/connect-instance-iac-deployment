# s3.tf

resource "aws_s3_bucket" "connect_content_bucket" {
  count = local.create_new_bucket ? 1 : 0

  bucket = local.s3_connect_name
  tags   = var.tags
}

resource "aws_s3_bucket_ownership_controls" "content_bucket" {
  count  = local.create_new_bucket ? 1 : 0
  bucket = aws_s3_bucket.connect_content_bucket[0].id
  rule {
    object_ownership = "ObjectWriter"
  }
}

resource "aws_s3_bucket_acl" "content_bucket" {
  count = local.create_new_bucket ? 1 : 0

  bucket = aws_s3_bucket.connect_content_bucket[0].id
  acl    = "private"

  depends_on = [aws_s3_bucket_ownership_controls.content_bucket[0]]
}

resource "aws_s3_bucket_server_side_encryption_configuration" "content_bucket" {
  count = local.create_new_bucket ? 1 : 0

  bucket = aws_s3_bucket.connect_content_bucket[0].id

  rule {
    bucket_key_enabled = true
    apply_server_side_encryption_by_default {
      kms_master_key_id = var.s3_encryption_cmk != null ? var.s3_encryption_cmk : null
      sse_algorithm     = var.s3_encryption_cmk != null ? "aws:kms" : "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "content_bucket" {
  count = local.create_new_bucket ? 1 : 0

  bucket = aws_s3_bucket.connect_content_bucket[0].id

  versioning_configuration {
    status     = "Suspended"
    mfa_delete = "Disabled"
  }
}

resource "aws_s3_bucket_public_access_block" "content_bucket" {
  count = local.create_new_bucket ? 1 : 0

  bucket = aws_s3_bucket.connect_content_bucket[0].id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
