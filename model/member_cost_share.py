import json
import uuid
from model.base_dynamo_model import BaseDynamoModel
from constants.constants import MemberCostShareKeys
from constants.json_constants import JsonMemberCostShareKeys


class MemberCostShare(BaseDynamoModel):

    partition_key = 'member_cost_share'

    @classmethod
    def from_json(cls, json_data):
        formatted_json = super().from_json(json_data=json_data)
        return cls(**formatted_json)

    @classmethod
    def from_dynamo(cls, dynamo_object):
        if dynamo_object is None:
            return None
        return cls(**dynamo_object)

    def __init__(self,
                 object_type,
                 object_id=None,
                 deductible=None,
                 copay=None,
                 org=None):
        self.object_id = object_id or uuid.uuid4().hex
        self.object_type = MemberCostShare.partition_key
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

    def to_dict(self):
        return {
            JsonMemberCostShareKeys.OBJECT_TYPE: JsonMemberCostShareKeys.OBJECT_TYPE_OUT,
            JsonMemberCostShareKeys.OBJECT_ID: self.object_id,
            JsonMemberCostShareKeys.DEDUCTIBLE: self.deductible,
            JsonMemberCostShareKeys.COPAY: self.copay,
            JsonMemberCostShareKeys.ORG: self.org,
        }
