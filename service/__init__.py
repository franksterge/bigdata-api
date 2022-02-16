from service.plan_service import PlanService
from storage_service import base_dynamo_service

plan_service = PlanService(base_dynamo_service)