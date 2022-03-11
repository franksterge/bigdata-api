"""
: Base Dynamo model.
"""
import uuid
from constants.json_constants import JsonBaseModelKeys
from constants.constants import BaseModelKeys


class BaseDynamoModel:

    @classmethod
    def from_json(cls, json_data):
        """
        : Converts json dictionary to BaseDynamoModel.
        """
        json_data[BaseModelKeys.OBJECT_ID] = json_data[JsonBaseModelKeys.OBJECT_ID]
        json_data[BaseModelKeys.OBJECT_TYPE] = json_data[JsonBaseModelKeys.OBJECT_TYPE]
        json_data[BaseModelKeys.ORG] = json_data[JsonBaseModelKeys.ORG]
        del json_data[JsonBaseModelKeys.OBJECT_ID]
        del json_data[JsonBaseModelKeys.OBJECT_TYPE]
        del json_data[JsonBaseModelKeys.ORG]
        return json_data

    def to_json(self):
        """
        : Returns the dictionary representation of this object
        : as a JSON string.
        """
        return self.to_dict()

    def __init__(self, object_id, object_type):
        self.object_id = object_id or uuid.uuid4().hex
        self.object_type = object_type

    def to_dict(self):
        """
        : Returns dictionary for this object.
        """
        return dict(filter(lambda kvp: kvp[1], self.__dict__.items()))

    def to_dynamo(self):
        return self.to_dict()

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        if set(self.to_dict().keys()) != set(other.to_dict().keys()):
            return False
        for key in self.to_dict().keys():
            if self.to_dict().get(key) != other.to_dict().get(key):
                return False
        return True

    def __hash__(self):
        return hash(self.__str__())
