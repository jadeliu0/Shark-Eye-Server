import boto3
import enum
import logging
from botocore.exceptions import ClientError
from urlparse import urlparse
import os
	
class FileType(enum.Enum):
    model = 1
    upload = 2


def getS3Bucket(fileType):
    if fileType==FileType.model:
        return "msi-sharkeye-model"
    else:
        return "msi-sharkeye-upload"
    	    

def upload(filePath, fileName, type=FileType.upload):
    if filePath is None:
        logging.error("please provide a valid filePath")
        return ''
    s3_client = boto3.client('s3')
    try:
        bucket = getS3Bucket(type)
        response = s3_client.upload_file(filePath, bucket, fileName)
        return "s3://"+bucket+'/'+fileName
    except ClientError as e:
        logging.error(e)
        return ''
    return ''

def download(s3Url, fileDir):
    if s3Url is None:
        logging.error("please provide a valid s3 url")
        return ''
    s3_client = boto3.client('s3')
    try:
        o = urlparse(s3Url)
        bucket = o.netloc
        key = o.path.lstrip('/')
        print bucket
        print key
        destPath = os.path.join(fileDir, key)
        s3_client.download_file(bucket, key, destPath)
        return destPath
    except ClientError as e:
        logging.error(e)
        return '' 
