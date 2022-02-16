class JsonBaseModelKeys:
    OBJECT_ID = 'objectId'
    OBJECT_TYPE = 'objectType'
    ORG = '_org'


class JsonMedicalServiceKeys(JsonBaseModelKeys):
    ORG = '_org'
    NAME = 'name'
    OBJECT_TYPE_OUT = 'service'


class JsonMemberCostShareKeys(JsonBaseModelKeys):
    ORG = '_org'
    COPAY = 'copay'
    DEDUCTIBLE = 'deductible'
    OBJECT_TYPE_OUT = 'membercostshare'


class JsonPlanServiceKeys(JsonBaseModelKeys):
    ORG = '_org'
    LINKED_SERVICE = 'linkedService'
    PLAN_SERVICE_COST_SHARES = 'planserviceCostShares'
    OBJECT_TYPE_OUT = 'planservice'


class JsonPlanKeys(JsonBaseModelKeys):
    PLAN = 'plan'
    ORG = '_org'
    PLAN_TYPE = 'planType'
    CREATION_DATE = 'creationDate'
    PLAN_COST_SHARES = 'planCostShares'
    LINKED_PLAN_SERVICES = 'linkedPlanServices'
    OBJECT_TYPE_OUT = 'plan'
