import os
import boto3
from constants.error_lib import BackEndException, ErrorCodes, ErrorMessages
from storage_service.base_dynamo_service import BaseDynamoService

dynamodb_table_name = os.getenv('DYNAMODB_TABLE_NAME', 'info7255')
region_name = os.getenv('REGION_NAME', 'us-east-2')
aws_key = os.getenv('AWS_ACCESS_KEY_ID', '')
aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY', '')
print(dynamodb_table_name)
print(region_name)
print(aws_key)
print(aws_secret_key)

dynamodb = boto3.resource("dynamodb",
                          aws_access_key_id=aws_key,
                          aws_secret_access_key=aws_secret_key,
                          region_name=region_name)
dynamodb_table = dynamodb.Table(dynamodb_table_name)

base_dynamo_service = BaseDynamoService(dynamo_table=dynamodb_table)

