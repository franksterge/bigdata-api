'''
: Services that interfaces with dynamoDB
'''
from storage_service.base_dynamo_service import BaseDynamoService
from constants.constants import DynamoKeys
from constants.error_lib import BackEndException, ErrorCodes, ErrorMessages


class PlanService(BaseDynamoService):

    def __init__(self, dynamo_table):
        super().__init__(dynamo_table=dynamo_table)

