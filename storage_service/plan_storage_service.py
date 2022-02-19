'''
: Services that interfaces with dynamoDB
'''

from boto3.dynamodb.conditions import Key
from storage_service.base_dynamo_service import BaseDynamoService
from model.plan import Plan
from model.plan_service import PlanService
from constants.constants import DynamoKeys, PlanServiceKeys
from constants.error_lib import BackEndException, ErrorCodes, ErrorMessages
from util.dynamo_util import query_dynamo_db


class PlanStorageService(BaseDynamoService):

    def __init__(self, dynamo_table):
        super().__init__(dynamo_table=dynamo_table)

    def get_plan(self, plan_id):
        response = self.get_dynamo_data(Plan.partition_key, plan_id)
        if DynamoKeys.CONTENT not in response.keys():
            raise BackEndException(
                ErrorMessages.PLAN_NOT_FOUND,
                ErrorCodes.NOT_FOUND)
        return Plan.from_dynamo(response[DynamoKeys.CONTENT])

    def get_linked_plan_services(self, service_ids):
        key_condition_expression = Key(
            DynamoKeys.PARTITION_KEY).eq(
            PlanService.partition_key)
        response = query_dynamo_db(
            table=self.dynamo_table,
            partition_key=key_condition_expression
        )
        if response is not None:
            plan_services = list(filter(lambda plan_service: plan_service[PlanServiceKeys.SORT_KEY] in service_ids, response))
            return plan_services
        return None
