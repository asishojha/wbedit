from storages.backends.s3boto3 import S3Boto3Storage


class S3MediaStorage(S3Boto3Storage):
    bucket_name = "wbedit-profile-pictures"
    location = ""
    region_name = "ap-south-1"
    signature_version = "s3v4"
    addressing_style = "path"
