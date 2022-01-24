# from storages.backends.gcloud import GoogleCloudStorage
#
#
# class StaticRootGoogleCloudStorage(GoogleCloudStorage):
#     location = "static"
#     default_acl = "publicRead"
#
#
# class MediaRootGoogleCloudStorage(GoogleCloudStorage):
#     location = "media"
#     file_overwrite = False

from storages.backends.s3boto3 import S3Boto3Storage


class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = "media"
    file_overwrite = False
