"""
: functional service for employee plans
"""
from constants.json_constants import JsonPlanKeys, JsonPlanServiceKeys
from model.plan import Plan
from model.plan_service import PlanService
from constants.error_lib import BackEndException, ErrorCodes, ErrorMessages
from util.patch_util import merge_data
from util.elasticsearch_util import process_es_data

class PlanFunctionalService:

    def __init__(self, plan_service, plan_service_service, medical_service_service, member_cost_share_service):
        self.plan_storage_service = plan_service
        self.plan_service_storage_service = plan_service_service
        self.medical_service_storage_service = medical_service_service
        self.member_cost_share_storage_service = member_cost_share_service

    def create_plan(self, plan_dict):
        if plan_dict is None:
            raise BackEndException(
                ErrorMessages.BAD_DATA,
                ErrorCodes.BAD_REQUEST)

        # TODO: ADD CHECK FOR IF PLAN ALREADY EXIST (THROW 409 CONFLICT IF YES)

        new_plan = Plan.from_json(plan_dict)
        new_plan_index = new_plan.to_index()
        process_es_data(index_data=new_plan_index)

        if new_plan.plan_cost_shares:
            self.plan_storage_service.create_dynamo_data(new_plan.plan_cost_shares)
            plan_cost_share_index = new_plan.plan_cost_shares.to_index(parent_attribute=JsonPlanKeys.PLAN_COST_SHARES,
                                                                       parent_id=new_plan.object_id)
            process_es_data(index_data=plan_cost_share_index, routing=new_plan.object_id)
        if new_plan.linked_plan_services:
            self.create_linked_plan_services(plan_services=new_plan.linked_plan_services, routing_id=new_plan.object_id)
            self.plan_storage_service.batch_write_data(new_plan.linked_plan_services)

        self.plan_storage_service.create_dynamo_data(new_plan)
        return new_plan

    def create_linked_plan_services(self, plan_services, routing_id):
        for plan_service in plan_services:
            plan_service_index = plan_service.to_index(parent_attribute=JsonPlanKeys.LINKED_PLAN_SERVICES,
                                                       parent_id=routing_id)
            linked_service_index = plan_service.linked_service.to_index(parent_attribute=JsonPlanServiceKeys.LINKED_SERVICE,
                                                                        parent_id=plan_service.object_id)
            plan_cost_share_index = plan_service.plan_service_cost_shares.to_index(
                parent_attribute=JsonPlanServiceKeys.PLAN_SERVICE_COST_SHARES,
                parent_id=plan_service.object_id)
            process_es_data(index_data=plan_service_index, routing=routing_id)
            process_es_data(index_data=linked_service_index, routing=routing_id)
            process_es_data(index_data=plan_cost_share_index, routing=routing_id)
            self.plan_storage_service.create_dynamo_data(plan_service.linked_service)
            self.plan_storage_service.create_dynamo_data(plan_service.plan_service_cost_shares)
            self.plan_storage_service.create_dynamo_data(plan_service)

    def get_plan(self, plan_id):
        # get plan object from dynamo
        # parse plan object to get cost shares and linked services
        plan = self.plan_storage_service.get_plan(plan_id=plan_id)
        plan_cost_shares_id = plan.plan_cost_shares
        linked_plan_services_ids = plan.linked_plan_services
        plan_cost_shares = self.get_plan_cost_shares(plan_cost_shares_id)
        linked_plan_services = self.get_linked_plan_services(linked_plan_services_ids)
        plan.plan_cost_shares = plan_cost_shares
        plan.linked_plan_services = linked_plan_services
        return plan

    def get_plan_cost_shares(self, object_id):
        return self.member_cost_share_storage_service.get_member_cost_share_object(object_id)

    def get_linked_plan_services(self, service_ids):
        response = self.plan_storage_service.get_linked_plan_services(service_ids)
        linked_plan_services = []
        for plan_service in response:
            new_plan_service = PlanService.from_dynamo(plan_service)

            medical_service_id = new_plan_service.linked_service
            plan_cost_share_id = new_plan_service.plan_service_cost_shares

            new_medical_service = self.medical_service_storage_service.get_medical_service_object(medical_service_id)
            new_member_cost_shares = self.member_cost_share_storage_service.get_member_cost_share_object(plan_cost_share_id)

            new_plan_service.linked_service = new_medical_service
            new_plan_service.plan_service_cost_shares = new_member_cost_shares

            linked_plan_services.append(new_plan_service)
        return linked_plan_services

    def delete_plan(self, object_id):
        plan = self.plan_storage_service.get_plan(plan_id=object_id)
        if plan is None:
            raise BackEndException(
                ErrorMessages.PLAN_NOT_FOUND,
                ErrorCodes.NOT_FOUND)
        self.plan_storage_service.delete_dynamo_data(object_type=Plan.partition_key, object_id=object_id)

    def patch_plan(self, object_id, new_plan_dict):
        plan = self.get_plan(object_id)
        if plan is None:
            raise BackEndException(
                ErrorMessages.PLAN_NOT_FOUND,
                ErrorCodes.NOT_FOUND)
        plan_dict = plan.to_json()
        plan_dict = merge_data(plan_dict, new_plan_dict)

        plan = self.create_plan(plan_dict)
        return plan
