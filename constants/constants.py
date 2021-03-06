class BaseModelKeys:
    OBJECT_ID = 'object_id'
    OBJECT_TYPE = 'object_type'
    ORG = 'org'
    PLAN_JOIN = 'plan_join'
    PLAN_JOIN_NAME = 'name'
    PLAN_JOIN_PARENT = 'parent'


class DynamoKeys:
    PARTITION_KEY = 'object_type'
    SORT_KEY = 'object_id'
    CONTENT = 'Item'
    BATCH_CONTENTS = 'Items'


class MedicalServiceKeys(BaseModelKeys, DynamoKeys):
    ORG = 'org'
    NAME = 'name'


class MemberCostShareKeys(BaseModelKeys, DynamoKeys):
    ORG = 'org'
    COPAY = 'copay'
    DEDUCTIBLE = 'deductible'


class PlanServiceKeys(BaseModelKeys, DynamoKeys):
    ORG = 'org'
    LINKED_SERVICE = 'linked_service'
    PLAN_SERVICE_COST_SHARES = 'plan_service_cost_shares'


class PlanKeys(BaseModelKeys, DynamoKeys):
    PLAN_COST_SHARES = 'plan_cost_shares'
    LINKED_PLAN_SERVICES = 'linked_plan_services'
    ORG = 'org'
    PLAN_TYPE = 'plan_type'
    CREATION_DATE = 'creation_date'
    PLAN_SERVICES_KEY = 'S'


class ElasticsearchSettings:
    HOST = 'localhost'
    PORT = 9200
    SCHEME = 'https'
    DOCKER_HOST = 'host.docker.internal'
