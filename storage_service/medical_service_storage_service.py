'''
: Services that interfaces with dynamoDB
'''
from storage_service.base_dynamo_service import BaseDynamoService
from model.medical_service import MedicalService
from constants.constants import DynamoKeys
from constants.error_lib import BackEndException, ErrorCodes, ErrorMessages


class MedicalServiceStorageService(BaseDynamoService):

    def __init__(self, dynamo_table):
        super().__init__(dynamo_table=dynamo_table)

    def get_medical_service_object(self, service_id):
        response = self.get_dynamo_data(MedicalService.partition_key, service_id)
        if response is None:
            raise BackEndException(
                ErrorMessages.SERVICE_NOT_FOUND,
                ErrorCodes.NOT_FOUND)
        return MedicalService.from_dynamo(response[DynamoKeys.CONTENT])
