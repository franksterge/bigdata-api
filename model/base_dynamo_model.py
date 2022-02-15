"""
: Base Dynamo model.
"""

import json
import decimal


class BaseDynamoModel:

    @classmethod
    def from_json(cls, json_data):
        """
        : Converts json dictionary to BaseDynamoModel.
        """
        return cls(**json_data)

    def to_json(self):
        """
        : Returns the dictionary representation of this object
        : as a JSON string.
        """
        return json.dumps(
            self.to_dict(),
            sort_keys=True,
            indent=4,
            default=self.decimal_default)

    def __init__(self, object_id, object_type):
        self.object_id = object_id
        self.object_type = object_type

    # Add the helper function for preventing error from having Decimal in
    # to_json
    def decimal_default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        raise TypeError

    def to_dict(self):
        """
        : Returns dictionary for this object.
        """
        return dict(filter(lambda kvp: kvp[1], self.__dict__.items()))

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
