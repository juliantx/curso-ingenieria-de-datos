provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "bucket1" {
  bucket = "mi-bucket-terraform-001"
}

resource "aws_s3_bucket" "bucket2" {
  bucket = "mi-bucket-terraform-002"
}