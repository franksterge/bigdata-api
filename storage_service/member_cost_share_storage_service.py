'''
: Services that interfaces with dynamoDB
'''
from storage_service.base_dynamo_service import BaseDynamoService
from model.member_cost_share import MemberCostShare
from constants.constants import DynamoKeys
from constants.error_lib import BackEndException, ErrorCodes, ErrorMessages


class MemberCostShareStorageService(BaseDynamoService):

    def __init__(self, dynamo_table):
        super().__init__(dynamo_table=dynamo_table)

    def get_member_cost_share_object(self, object_id):
        response = self.get_dynamo_data(MemberCostShare.partition_key, object_id)
        if response is None:
            raise BackEndException(
                ErrorMessages.MEMBER_COST_SHARE_NOT_FOND,
                ErrorCodes.NOT_FOUND)
        return MemberCostShare.from_dynamo(response[DynamoKeys.CONTENT])
