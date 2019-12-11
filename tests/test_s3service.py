import unittest

import boto3
from moto import mock_s3

from s3service import S3Service


class S3ServiceTestCase(unittest.TestCase):
    """Test Class for S3Services
    """

    @classmethod
    def setUpClass(self):
        self._client = boto3.client(
            "s3", aws_access_key_id="mock_access_key", aws_secret_access_key="mock_secret_key")
        self._bucket = "mock_bucket"
        self._table = "mock_table"
        self._date = "20191121"
        self._prefix = f'{self._table}/{self._date}/'

    def _put_mock_file(self):
        conn = boto3.resource("s3", region_name="asia-northeast-1")
        conn.create_bucket(Bucket=self._bucket)
        conn.Bucket(self._bucket).put_object(
            Key=f"{self._prefix}test.tsv.gz", Body="test")

    def test_init(self):
        s = S3Service(client=self._client, bucket=self._bucket,
                      table=self._table, date=self._date)

        self.assertEqual(self._client, s._client)
        self.assertEqual(self._bucket, s._bucket)
        self.assertEqual(self._table, s._table)
        self.assertEqual(self._date, s._date)
        self.assertEqual(self._prefix, s._prefix)

    @mock_s3
    def test_get_list_object_contents(self):
        s = S3Service(client=self._client, bucket=self._bucket,
                      table=self._table, date=self._date)
        self._put_mock_file()

        actual = s.get_list_object_contents()
        self.assertEqual("mock_table/20191121/test.tsv.gz", actual[0]["Key"])

    @mock_s3
    def test_get_list_object_contents_failure(self):
        s = S3Service(client=self._client, bucket=self._bucket,
                      table=self._table, date=self._date)

        actual = s.get_list_object_contents()
        self.assertIsNone(actual)

    @mock_s3
    def test_get_object(self):
        s = S3Service(client=self._client, bucket=self._bucket,
                      table=self._table, date=self._date)
        self._put_mock_file()

        actual = s.get_object(key="mock_table/20191121/test.tsv.gz")
        body = actual["Body"].read().decode("utf-8")
        self.assertEqual("test", body)

    @mock_s3
    def test_get_object_failure(self):
        s = S3Service(client=self._client, bucket=self._bucket,
                      table=self._table, date=self._date)

        actual = s.get_object(key="mock_table/20191121/test.tsv.gz")
        self.assertIsNone(actual)

    @mock_s3
    def test_put_object(self):
        s = S3Service(client=self._client, bucket=self._bucket,
                      table=self._table, date=self._date)
        conn = boto3.resource("s3", region_name="asia-northeast-1")
        conn.create_bucket(Bucket=self._bucket)

        result = s.put_object(
            key="mock_table/20191121/test.tsv.gz", body=b"hello")
        self.assertTrue(result)

        actual = conn.Object(
            'mock_bucket', 'mock_table/20191121/test.tsv.gz').get()['Body'].read().decode("utf-8")
        self.assertEqual(actual, "hello")

    @mock_s3
    def test_put_object_failure(self):
        s = S3Service(client=self._client, bucket=self._bucket,
                      table=self._table, date=self._date)

        result = s.put_object(
            key="mock_table/20191121/test.tsv.gz", body=b"hello")
        self.assertFalse(result)
