'''
： Data model for plan
'''
from model.base_dynamo_model import BaseDynamoModel
from model.member_cost_share import MemberCostShare
from model.plan_service import PlanService
from constants.constants import PlanKeys
from constants.json_constants import JsonPlanKeys


class Plan(BaseDynamoModel):

    partition_key = 'plan'

    @classmethod
    def from_json(cls, json_data):
        formatted_json = super().from_json(json_data=json_data)
        formatted_json[PlanKeys.PLAN_TYPE] = json_data[JsonPlanKeys.PLAN_TYPE]
        formatted_json[PlanKeys.CREATION_DATE] = json_data[JsonPlanKeys.CREATION_DATE]
        del json_data[JsonPlanKeys.PLAN_TYPE], json_data[JsonPlanKeys.CREATION_DATE]

        plan_cost_shares = {}
        linked_plan_services = []
        if formatted_json[JsonPlanKeys.PLAN_COST_SHARES]:
            plan_cost_shares = formatted_json[JsonPlanKeys.PLAN_COST_SHARES]
            del formatted_json[JsonPlanKeys.PLAN_COST_SHARES]
        if formatted_json[JsonPlanKeys.LINKED_PLAN_SERVICES]:
            linked_plan_services = formatted_json[JsonPlanKeys.LINKED_PLAN_SERVICES]
            del formatted_json[JsonPlanKeys.LINKED_PLAN_SERVICES]

        plan = cls(**formatted_json)

        plan.set_plan_cost_shares(plan_cost_shares=plan_cost_shares)
        plan.set_linked_plan_services(linked_plan_services=linked_plan_services)

        return plan

    @classmethod
    def from_dynamo(cls, dynamo_object):
        if dynamo_object is None:
            return None
        return cls(**dynamo_object)

    def __init__(self,
                 object_type,
                 object_id=None,
                 org=None,
                 plan_type=None,
                 creation_date=None,
                 plan_cost_shares=None,
                 linked_plan_services=None):
        self.object_id = object_id
        self.object_type = Plan.partition_key
        self.org = org
        self.plan_type = plan_type
        self.creation_date = creation_date
        self.plan_cost_shares = plan_cost_shares
        self.linked_plan_services = linked_plan_services or []

    def set_linked_plan_services(self, linked_plan_services=None):
        if type(linked_plan_services) is list:
            for plan_service in linked_plan_services:
                self.linked_plan_services.append(PlanService.from_json(plan_service))
            # self.linked_plan_services.append(PlanService.from_json(x) for x in linked_plan_services)
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
            PlanKeys.PLAN_COST_SHARES: self.plan_cost_shares.object_id,
            PlanKeys.LINKED_PLAN_SERVICES: [x.object_id for x in self.linked_plan_services],
        }

    def to_dict(self):
        return {
            PlanKeys.OBJECT_TYPE: JsonPlanKeys.OBJECT_TYPE_OUT,
            PlanKeys.OBJECT_ID: self.object_id,
            PlanKeys.ORG: self.org,
            PlanKeys.PLAN_TYPE: self.plan_type,
            PlanKeys.CREATION_DATE: self.creation_date,
            PlanKeys.PLAN_COST_SHARES: self.plan_cost_shares.to_dict(),
            PlanKeys.LINKED_PLAN_SERVICES: [x.to_dict() for x in self.linked_plan_services],
        }
