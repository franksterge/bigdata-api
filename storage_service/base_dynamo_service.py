'''
: Services that interfaces with dynamoDB
'''

from constants.constants import DynamoKeys
from constants.error_lib import BackEndException, ErrorCodes, ErrorMessages
from model.base_dynamo_model import BaseDynamoModel


class BaseDynamoService:
    def __init__(self, dynamo_table):
        self.dynamo_table = dynamo_table

    def get_dynamo_data(self, pkey, skey):
        if pkey is None or skey is None:
            raise BackEndException(
                ErrorMessages.BAD_DATA,
                ErrorCodes.BAD_REQUEST)
        response = self.dynamo_table.get_item(
            Key={
                DynamoKeys.PARTITION_KEY: pkey,
                DynamoKeys.SORT_KEY: skey
            }
        )
        return response

    def create_dynamo_data(self, payload_obj):
        if payload_obj is None:
            raise BackEndException(
                ErrorMessages.BAD_DATA,
                ErrorCodes.BAD_REQUEST)
        if not isinstance(payload_obj, BaseDynamoModel):
            raise BackEndException(
                ErrorMessages.BAD_DATA,
                ErrorCodes.SERVER_ERROR)

        self.dynamo_table.put_item(Item=payload_obj.to_dynamo())
        return payload_obj.to_dynamo()

    def delete_dynamo_data(self, payload_obj):
        if payload_obj is None:
            raise BackEndException(
                ErrorMessages.BAD_DATA,
                ErrorCodes.BAD_REQUEST)
        if not isinstance(payload_obj, BaseDynamoModel):
            raise BackEndException(
                ErrorMessages.BAD_DATA,
                ErrorCodes.SERVER_ERROR)

        self.dynamo_table.delete_item(
            Key={
                DynamoKeys.PARTITION_KEY: payload_obj.object_type,
                DynamoKeys.SORT_KEY: payload_obj.object_id
            }
        )

    def batch_write_data(self, payload_list):
        if payload_list is None:
            raise BackEndException(
                ErrorMessages.BAD_DATA,
                ErrorCodes.BAD_REQUEST)
        with self.dynamo_table.batch_writer() as payload_writer:
            for item in payload_list:
                payload_writer.put_item(Item=item.to_dynamo())

    def get_batch_writer(self):
        return self.dynamo_table.batch_writer()