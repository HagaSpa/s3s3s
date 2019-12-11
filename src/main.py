import os
import time
import logging
from datetime import datetime, timedelta, timezone

import boto3

from s3service import S3Service


def main():
    """
    Put all objects in src_bucket/table/date/* into dest_bucket/table/date/*
    """
    d = create_env_dict()

    src_client = boto3.client(
        "s3", aws_access_key_id=d["src_access_key"], aws_secret_access_key=d["src_secret_key"])
    dest_client = boto3.client(
        "s3", aws_access_key_id=d["dest_access_key"], aws_secret_access_key=d["dest_secret_key"])

    # Initialize Service
    src_service = S3Service(
        client=src_client, bucket=d["src_bucket"], table=d["table"], date=d["date"])
    dest_service = S3Service(
        client=dest_client, bucket=d["dest_bucket"], table=d["table"], date=d["date"])

    # Get Contents
    src_contents = src_service.get_list_object_contents()
    if src_contents is None:
        logging.error(f"No Object. s3://{d['src_bucket']}")
        raise

    # Get the object and place the memory in bytes
    for c in src_contents:
        obj = src_service.get_object(key=c["Key"])
        if obj is None:
            logging.error(
                f"Failed Get: {c['Key']}. s3://{d['src_bucket']}")
            raise

        success = dest_service.put_object(
            key=c["Key"], body=obj["Body"].read())
        if not success:
            logging.error(
                f"Failed Add: {c['Key']}. s3://{d['src_bucket']} to s3://{d['dest_bucket']} ")
            raise

        logging.info(
            f"Success: {c['Key']}. s3://{d['src_bucket']} to s3://{d['dest_bucket']} ")


def create_env_dict() -> dict:
    """
    get environment value.
    """
    d = dict()
    # require environment parameter
    d["src_bucket"] = os.environ["src_bucket"]
    d["dest_bucket"] = os.environ["dest_bucket"]
    d["table"] = os.environ["table"]

    # optional environment prameter
    d["src_access_key"] = os.getenv("src_access_key", default=None)
    d["src_secret_key"] = os.getenv("src_secret_key", default=None)
    d["dest_access_key"] = os.getenv("dest_access_key", default=None)
    d["dest_secret_key"] = os.getenv("dest_secret_key", default=None)
    d["date"] = os.getenv("date",
                          default=datetime.strftime(datetime.now(timezone(timedelta(hours=+9), "JST")) - timedelta(days=1), "%Y%m%d"))
    return d


if __name__ == '__main__':
    # Set up logging
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(asctime)s: %(message)s')
    start = time.time()
    # main
    main()
    t = time.time() - start
    print("elasped time（sec）: ", t)
