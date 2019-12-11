import logging

from botocore.exceptions import ClientError


class S3Service():
    """S3 Service
    """

    def __init__(self, client, bucket, table, date):
        self._client = client
        self._bucket = bucket
        self._table = table
        self._date = date
        self._prefix = "{}/{}/".format(self._table, self._date)

    def get_list_object_contents(self):
        """Get Contents

        Note: Contents counts limit 1000 max
        """
        try:
            response = self._client.list_objects_v2(
                Bucket=self._bucket, Prefix=self._prefix, StartAfter=self._prefix, Delimiter='/')
        except ClientError as e:
            logging.error(e)
            return None
        return response["Contents"] if response["KeyCount"] > 0 else None

    def get_object(self, key: str):
        """Get Object
        """
        try:
            obj = self._client.get_object(Bucket=self._bucket, Key=key)
        except ClientError as e:
            logging.error(e)
            return None
        return obj

    def put_object(self, key: str, body: bytes):
        """Put Object
        """
        try:
            self._client.put_object(
                Bucket=self._bucket, Key=key, Body=body)
        except ClientError as e:
            logging.error(e)
            return False
        return True
