'''
： Data model for plan
'''
import uuid
from model.base_dynamo_model import BaseDynamoModel
from model.member_cost_share import MemberCostShare
from model.plan_service import PlanService
from constants.constants import PlanKeys
from constants.json_constants import JsonPlanKeys

class Plan(BaseDynamoModel):

    partition_key = 'plan'

    @classmethod
    def from_json(cls, json_data):
        json_data[PlanKeys.OBJECT_ID] = json_data[JsonPlanKeys.OBJECT_ID]
        json_data[PlanKeys.OBJECT_TYPE] = json_data[JsonPlanKeys.OBJECT_TYPE]
        json_data[PlanKeys.ORG] = json_data[JsonPlanKeys.ORG]

        plan = cls(**json_data)

        plan_cost_shares = json_data[JsonPlanKeys.PLAN_COST_SHARES] \
            if json_data[JsonPlanKeys.PLAN_COST_SHARES] else None
        plan.set_plan_cost_shares(plan_cost_shares=plan_cost_shares)

        linked_plan_services = json_data[JsonPlanKeys.LINKED_PLAN_SERVICES] \
            if json_data[JsonPlanKeys.LINKED_PLAN_SERVICES] else None
        plan.set_linked_plan_services(linked_plan_services=linked_plan_services)

        return plan

    @classmethod
    def from_dynamo(cls, dynamo_object):
        if dynamo_object is None:
            return None

        plan = cls(**dynamo_object)

        plan_cost_shares = dynamo_object[PlanKeys.PLAN_COST_SHARES] \
            if dynamo_object[PlanKeys.PLAN_COST_SHARES] else None
        plan.set_plan_cost_shares(plan_cost_shares=plan_cost_shares)

        linked_plan_services = dynamo_object[PlanKeys.LINKED_PLAN_SERVICES] \
            if dynamo_object[PlanKeys.LINKED_PLAN_SERVICES] else None
        plan.set_linked_plan_services(linked_plan_services=linked_plan_services)

        return plan


    def __init__(self,
                 object_type,
                 object_id=None,
                 org=None,
                 plan_type=None,
                 creation_date=None,
                 plan_cost_shares=None,
                 linked_plan_services=None):
        self.object_id = object_id or uuid.uuid4().hex
        self.object_type = object_type
        self.org = org
        self.plan_type = plan_type
        self.creation_date = creation_date
        self.plan_cost_shares = plan_cost_shares
        self.linked_plan_services = linked_plan_services or []

    def set_linked_plan_services(self, linked_plan_services=None):
        if type(linked_plan_services) is list:
            self.linked_plan_services.append(lambda x: PlanService.from_json(x))
        else:
            self.linked_plan_services = []

    def set_plan_cost_shares(self, plan_cost_shares):
        self.plan_cost_shares = MemberCostShare.from_json(plan_cost_shares) \
            if plan_cost_shares else None

    def to_dynamo(self):
        return {
            PlanKeys.PARTITION_KEY: self.object_type,
            PlanKeys.SORT_KEY: self.object_id,
            PlanKeys.ORG: self.org,
            PlanKeys.PLAN_TYPE: self.plan_type,
            PlanKeys.CREATION_DATE: self.creation_date,
            PlanKeys.PLAN_COST_SHARES: self.plan_cost_shares.object_type + ':' + self.plan_cost_shares.object_id,
            PlanKeys.LINKED_PLAN_SERVICES: [(x.object_type + ':' + x.object_id) for x in self.linked_plan_services],
        }