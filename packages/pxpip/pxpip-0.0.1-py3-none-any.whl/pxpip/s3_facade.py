import os

import boto3

from pxpip.logger import logger

log = logger(__name__)

s3 = boto3.resource(
    "s3",
    endpoint_url=os.getenv("ENDPOINT_URL", None),
    region_name=os.getenv("AWS_REGION", None),
)


def download_file(bucket, key, local_dir="./"):
    s3_object = s3.Object(bucket, key)
    file_path = os.path.join(local_dir, os.path.basename(key))
    with open(file_path, "wb") as wf:
        wf.write(s3_object.get()["Body"].read())
        log.info(f"download complete for {bucket}/{key} to {local_dir}/{key}")

    return file_path


def upload_file(bucket, key, file_path):
    """Uploads a local file system file to the provided S3 config"""
    s3.meta.client.upload_file(file_path, bucket, key)
    log.info(f"upload complete for {bucket}/{key} from {file_path}")

