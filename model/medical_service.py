import uuid
from model.base_dynamo_model import BaseDynamoModel
from constants.constants import MedicalServiceKeys
from constants.json_constants import JsonMedicalServiceKeys


class MedicalService(BaseDynamoModel):

    partition_key = 'medical_service'

    @classmethod
    def from_json(cls, json_data):
        json_data[MedicalServiceKeys.OBJECT_ID] = json_data[JsonMedicalServiceKeys.OBJECT_ID]
        json_data[MedicalServiceKeys.OBJECT_TYPE] = json_data[JsonMedicalServiceKeys.OBJECT_TYPE]
        json_data[MedicalServiceKeys.ORG] = json_data[JsonMedicalServiceKeys.ORG]
        return cls(**json_data)

    @classmethod
    def from_dynamo(cls, dynamo_object):
        if dynamo_object is None:
            return None
        return MedicalService(
            object_type=dynamo_object.get(MedicalServiceKeys.OBJECT_TYPE),
            object_id=dynamo_object.get(MedicalServiceKeys.OBJECT_ID),
            name=dynamo_object.get(MedicalServiceKeys.NAME),
            org=dynamo_object.get(MedicalServiceKeys.ORG)
        )

    def __init__(self,
                 object_type,
                 object_id=None,
                 name=None,
                 org=None):
        self.object_id = object_id or uuid.uuid4().hex
        self.object_type = object_type
        self.name = name
        self.org = org

    def to_dynamo(self):
        return {
            MedicalServiceKeys.PARTITION_KEY: self.object_type,
            MedicalServiceKeys.SORT_KEY: self.object_id,
            MedicalServiceKeys.NAME: self.name,
            MedicalServiceKeys.ORG: self.org,
        }
