
# connect.tf
resource "aws_connect_instance" "connect_instance" {
  instance_alias                   = local.instance_name
  identity_management_type         = var.connect_identity_management_type
  directory_id                     = var.connect_identity_management_type == "EXISTING_DIRECTORY" ? var.connect_existing_directory_id : null
  inbound_calls_enabled            = var.inbound_calls_enabled
  outbound_calls_enabled           = var.outbound_calls_enabled
  early_media_enabled              = var.early_media_enabled
  auto_resolve_best_voices_enabled = var.auto_resolve_best_voices_enabled
  contact_flow_logs_enabled        = var.contact_flow_logs_enabled
  contact_lens_enabled             = var.contact_lens_enabled
  multi_party_conference_enabled   = var.multi_party_conference_enabled
}

resource "aws_connect_instance_storage_config" "chat_transcripts" {
  instance_id   = aws_connect_instance.connect_instance.id
  resource_type = "CHAT_TRANSCRIPTS"

  storage_config {
    s3_config {
      bucket_name   = local.s3_storage_bucket_name
      bucket_prefix = "connect/${local.instance_name}/ChatTranscripts"

      # By default S3 will enforce the encrytion of all objects, so this is for consistency
      # and ensuring the outcome is expected with regard to permissions that the role must have.
      dynamic "encryption_config" {
        for_each = var.s3_encryption_cmk != null ? [1] : []
        content {
          encryption_type = "KMS"
          key_id          = var.s3_encryption_cmk
        }
      }
    }
    storage_type = "S3"
  }
}

resource "aws_connect_instance_storage_config" "call_recordings" {
  instance_id   = aws_connect_instance.connect_instance.id
  resource_type = "CALL_RECORDINGS"

  storage_config {
    s3_config {
      bucket_name   = local.s3_storage_bucket_name
      bucket_prefix = "connect/${local.instance_name}/CallRecordings"

      # By default S3 will enforce the encrytion of all objects, so this is for consistency
      # and ensuring the outcome is expected with regard to permissions that the role must have.
      dynamic "encryption_config" {
        for_each = var.s3_encryption_cmk != null ? [1] : []
        content {
          encryption_type = "KMS"
          key_id          = var.s3_encryption_cmk
        }
      }
    }
    storage_type = "S3"
  }
}

resource "aws_connect_instance_storage_config" "scheduled_reports" {
  instance_id   = aws_connect_instance.connect_instance.id
  resource_type = "SCHEDULED_REPORTS"

  storage_config {
    s3_config {
      bucket_name   = local.s3_storage_bucket_name
      bucket_prefix = "connect/${local.instance_name}/Reports"

      # By default S3 will enforce the encrytion of all objects, so this is for consistency
      # and ensuring the outcome is expected with regard to permissions that the role must have.
      dynamic "encryption_config" {
        for_each = var.s3_encryption_cmk != null ? [1] : []
        content {
          encryption_type = "KMS"
          key_id          = var.s3_encryption_cmk
        }
      }
    }
    storage_type = "S3"
  }
}
