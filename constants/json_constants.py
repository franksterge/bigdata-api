class JsonBaseModelKeys:
    OBJECT_ID = 'objectId'
    OBJECT_TYPE = 'objectType'


class JsonMedicalServiceKeys(JsonBaseModelKeys):
    ORG = '_org'
    NAME = 'name'


class JsonMemberCostShareKeys(JsonBaseModelKeys):
    ORG = '_org'
    COPAY = 'copay'
    DEDUCTIBLE = 'deductible'


class JsonPlanServiceKeys(JsonBaseModelKeys):
    ORG = '_org'
    LINKED_SERVICE = 'linkedService'
    PLAN_SERVICE_COST_SHARES = 'planServiceCostShares'


class JsonPlanKeys(JsonBaseModelKeys):
    ORG = '_org'
    PLAN_TYPE = 'planType'
    CREATION_DATE = 'creationDate'
    PLAN_COST_SHARES = 'planCostShares'
    LINKED_PLAN_SERVICES = 'linkedPlanServices'
