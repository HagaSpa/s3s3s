import os
import unittest
from datetime import datetime, timedelta, timezone

import boto3
from moto import mock_s3

from main import create_env_dict, main


class MainTestCase(unittest.TestCase):
    """Test Class for main
    """

    def setUp(self):
        os.environ["src_bucket"] = "src_bucket_test"
        os.environ["dest_bucket"] = "dest_bucket_test"
        os.environ["table"] = "table_test"
        os.environ["src_access_key"] = "src_access_key_test"
        os.environ["src_secret_key"] = "src_secret_key_test"
        os.environ["dest_access_key"] = "dest_access_key_test"
        os.environ["dest_secret_key"] = "dest_secret_key_test"
        os.environ["date"] = "20191211"

    def test_create_env_dict(self):
        expected = {
            "src_bucket": "src_bucket_test",
            "dest_bucket": "dest_bucket_test",
            "table": "table_test",
            "src_access_key": "src_access_key_test",
            "src_secret_key": "src_secret_key_test",
            "dest_access_key": "dest_access_key_test",
            "dest_secret_key": "dest_secret_key_test",
            "date": "20191211",
        }
        actual = create_env_dict()
        self.assertEqual(expected, actual)

    def test_create_env_dict_date(self):
        del os.environ["date"]
        actual = create_env_dict()
        expected = datetime.strftime(datetime.now(
            timezone(timedelta(hours=+9), "JST")) - timedelta(days=1), "%Y%m%d")
        self.assertEqual(expected, actual["date"])

    def test_create_env_dict_failure(self):
        del os.environ["src_bucket"]
        del os.environ["dest_bucket"]
        del os.environ["table"]
        with self.assertRaises(KeyError):
            create_env_dict()

    @mock_s3
    def test_main(self):
        # create test.tsv.gz in src s3
        src_bucket = os.environ["src_bucket"]
        key = f'{os.environ["table"]}/{os.environ["date"]}/test.tsv.gz'
        conn = boto3.resource("s3", region_name="asia-northeast-1")
        conn.create_bucket(Bucket=src_bucket)
        conn.Bucket(src_bucket).put_object(Key=key, Body="test")

        # create dest s3
        dest_bucket = os.environ["dest_bucket"]
        conn.create_bucket(Bucket=dest_bucket)

        main()

        # assert 
        dest_body = conn.Object(dest_bucket, key).get()[
            'Body'].read().decode("utf-8")
        self.assertEqual(dest_body, "test")
