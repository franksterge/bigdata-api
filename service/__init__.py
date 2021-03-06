from service.plan_functional_service import PlanFunctionalService
from storage_service import plan_service, plan_service_service, medical_service_service, member_cost_share_service

plan_service = PlanFunctionalService(plan_service,
                                     plan_service_service,
                                     medical_service_service,
                                     member_cost_share_service)