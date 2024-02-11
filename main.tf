terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region  = "eu-west-1"
}

resource "aws_s3_bucket" "ml-deploy" {
  bucket = "ml-deploy-bucket-1001"
  tags = {
    Name        = "ml-deploy-bucket-1001"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket_ownership_controls" "ml-deploy" {
  bucket = aws_s3_bucket.ml-deploy.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "ml-deploy" {
  depends_on = [aws_s3_bucket_ownership_controls.ml-deploy]

  bucket = aws_s3_bucket.ml-deploy.id
  acl    = "private"
}
