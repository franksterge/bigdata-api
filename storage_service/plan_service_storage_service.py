'''
: Services that interfaces with dynamoDB
'''
from storage_service.base_dynamo_service import BaseDynamoService
from model.plan_service import PlanService
from constants.constants import DynamoKeys
from constants.error_lib import BackEndException, ErrorCodes, ErrorMessages


class PlanServiceStorageService(BaseDynamoService):

    def __init__(self, dynamo_table):
        super().__init__(dynamo_table=dynamo_table)

    def get_plan_service_object(self, service_id):
        response = self.get_dynamo_data(PlanService.partition_key, service_id)
        if response is None:
            raise BackEndException(
                ErrorMessages.SERVICE_NOT_FOUND,
                ErrorCodes.NOT_FOUND)
        print(response)
        return PlanService.from_dynamo(response)
