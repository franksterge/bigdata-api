"""
: functional service for employee plans
"""
from model.plan import Plan
from constants.error_lib import BackEndException, ErrorCodes, ErrorMessages


class PlanService:

    def __init__(self, base_dynamo_service):
        self.base_dynamo_service = base_dynamo_service

    def create_plan(self, plan_dict):
        if plan_dict is None:
            raise BackEndException(
                ErrorMessages.BAD_DATA,
                ErrorCodes.BAD_REQUEST)

        new_plan = Plan.from_json(plan_dict)
        if new_plan.plan_cost_shares:
            self.base_dynamo_service.create_dynamo_data(new_plan.plan_cost_shares)
        if new_plan.linked_plan_services:
            self.create_linked_plan_services(new_plan.linked_plan_services)
            self.base_dynamo_service.batch_write_data(new_plan.linked_plan_services)

        self.base_dynamo_service.create_dynamo_data(new_plan)
        return new_plan


    def create_linked_plan_services(self, plan_services):
        for plan_service in plan_services:
            self.base_dynamo_service.create_dynamo_data(plan_service.linked_service)
            self.base_dynamo_service.create_dynamo_data(plan_service.plan_service_cost_shares)
            self.base_dynamo_service.create_dynamo_data(plan_service)


    # def get_plan(self, plan_id):
