'''
: Data model for plan service
'''
import uuid
from model.base_dynamo_model import BaseDynamoModel
from model.medical_service import MedicalService
from model.member_cost_share import MemberCostShare
from constants.constants import PlanServiceKeys
from constants.json_constants import JsonPlanServiceKeys

class PlanService(BaseDynamoModel) :

    partition_key = 'plan_service'

    @classmethod
    def from_json(cls, json_data):
        json_data[PlanServiceKeys.OBJECT_ID] = json_data[JsonPlanServiceKeys.OBJECT_ID]
        json_data[PlanServiceKeys.OBJECT_TYPE] = json_data[JsonPlanServiceKeys.OBJECT_TYPE]
        json_data[PlanServiceKeys.ORG] = json_data[JsonPlanServiceKeys.ORG]

        plan_service = cls(**json_data)

        linked_service = json_data[JsonPlanServiceKeys.LINKED_SERVICE] \
            if json_data[JsonPlanServiceKeys.LINKED_SERVICE] else None
        plan_service.set_linked_service(linked_service=linked_service)

        service_cost_share = json_data[JsonPlanServiceKeys.PLAN_SERVICE_COST_SHARES] \
            if json_data[JsonPlanServiceKeys.PLAN_SERVICE_COST_SHARES] else None
        plan_service.set_plan_service_cost_shares(plan_service_cost_shares=service_cost_share)

        return plan_service

    @classmethod
    def from_dynamo(cls, dynamo_object):
        if dynamo_object is None:
            return None

        plan_service = cls(**dynamo_object)

        linked_service = dynamo_object[PlanServiceKeys.LINKED_SERVICE] \
            if dynamo_object[PlanServiceKeys.LINKED_SERVICE] else None
        plan_service.set_linked_service(linked_service=linked_service)

        service_cost_share = dynamo_object[PlanServiceKeys.PLAN_SERVICE_COST_SHARES] \
            if dynamo_object[PlanServiceKeys.PLAN_SERVICE_COST_SHARES] else None
        plan_service.set_plan_service_cost_shares(plan_service_cost_shares=service_cost_share)

        return plan_service

    def __init__(self,
                 object_type,
                 object_id=None,
                 org=None):
        self.object_id = object_id or uuid.uuid4().hex
        self.object_type = object_type
        self.org = org
        self.linked_service = None
        self.plan_service_cost_shares = None

    def set_linked_service(self, linked_service=None):
        self.linked_service = MedicalService.from_json(linked_service) \
            if linked_service else None

    def set_plan_service_cost_shares(self, plan_service_cost_shares=None):
        self.plan_service_cost_shares = MemberCostShare.from_json(plan_service_cost_shares) \
            if plan_service_cost_shares else None

    def to_dynamo(self):
        return {
            PlanServiceKeys.PARTITION_KEY: self.object_type,
            PlanServiceKeys.SORT_KEY: self.object_id,
            PlanServiceKeys.ORG: self.org,
            PlanServiceKeys.LINKED_SERVICE: self.linked_service.partition_key + ':' + self.linked_service.object_id,
            PlanServiceKeys.PLAN_SERVICE_COST_SHARES: self.plan_service_cost_shares.object_type + ':' + self.plan_service_cost_shares.object_id,
        }