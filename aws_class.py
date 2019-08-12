class AWS:
    def __init__(self, access_key=None, secret_key=None):
        if secret_key is not None and access_key is not None:
            self.s3 = boto3.resource(
                's3',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
            )
            self.s3Client = boto3.client(
                's3',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
            )
        else:
            self.s3 = boto3.resource('s3')
            self.s3Client = boto3.client('s3')
            

    def upload_data(self, bucket: str = None, data: bytes = None, key: str = None):
        """
        Upload a Bytes[] data to S3
        :param bucket:
        :param data:
        :param key:
        """
        self.s3.Object(bucket_name=bucket, key=key).put(Body=data)


    def url(self, bucket: str, key: str):
        """
        Get HTTP url for a key oin bucket
        :param bucket:
        :param key:
        :return: url
        """
        url = self.s3Client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': bucket,
                'Key': key
            }
        )
        return urlsplit(url)._replace(query=None).geturl()
