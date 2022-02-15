import uuid
from model.base_dynamo_model import BaseDynamoModel
from constants.constants import MemberCostShareKeys
from constants.json_constants import JsonMemberCostShareKeys


class MemberCostShare(BaseDynamoModel):

    partition_key = 'member_cost_share'

    @classmethod
    def from_json(cls, json_data):
        json_data[MemberCostShareKeys.OBJECT_ID] = json_data[JsonMemberCostShareKeys.OBJECT_ID]
        json_data[MemberCostShareKeys.OBJECT_TYPE] = json_data[JsonMemberCostShareKeys.OBJECT_TYPE]
        json_data[MemberCostShareKeys.ORG] = json_data[MemberCostShareKeys.ORG]
        return cls(**json_data)

    @classmethod
    def from_dynamo(cls, dynamo_object):
        if dynamo_object is None:
            return None
        return MemberCostShare(
            object_type=dynamo_object.get(MemberCostShareKeys.OBJECT_TYPE),
            object_id=dynamo_object.get(MemberCostShareKeys.OBJECT_ID),
            deductible=dynamo_object.get(MemberCostShareKeys.DEDUCTIBLE),
            copay=dynamo_object.get(MemberCostShareKeys.COPAY),
            org=dynamo_object.get(MemberCostShareKeys.ORG)
        )

    def __init__(self,
                 object_type,
                 object_id=None,
                 deductible=None,
                 copay=None,
                 org=None):
        self.object_id = object_id or uuid.uuid4().hex
        self.object_type = object_type
        self.deductible = deductible
        self.copay = copay
        self.org = org

    def to_dynamo(self):
        return {
            MemberCostShareKeys.PARTITION_KEY: self.object_type,
            MemberCostShareKeys.SORT_KEY: self.object_id,
            MemberCostShareKeys.DEDUCTIBLE: self.deductible,
            MemberCostShareKeys.COPAY: self.copay,
            MemberCostShareKeys.ORG: self.org,
        }
