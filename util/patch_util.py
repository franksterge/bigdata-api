from constants.json_constants import JsonBaseModelKeys
from constants.error_lib import BackEndException, ErrorMessages, ErrorCodes


'''
: merges two dictionaries from json
:   Params:
:       current_dict: a dictionary of the plan that is reconstructed with full data entries in request/response format
:                     processed from dynamodb using to_dict() method of Plan
:       new_dict: a dictionary from the API body indicating what the patched data entries are 
'''
def merge_data(current_dict, new_dict):
    if type(new_dict) is list:
        for new_item in new_dict:
            if JsonBaseModelKeys.OBJECT_ID not in new_item.keys():
                raise BackEndException(
                    ErrorMessages.BAD_DATA,
                    ErrorCodes.BAD_REQUEST)
            current_item = next((x for x in current_dict if x[JsonBaseModelKeys.OBJECT_ID] == new_item[JsonBaseModelKeys.OBJECT_ID]), None)
            if current_item is None:
                current_dict.append(new_item)
            else:
                current_item = merge_data(current_item, new_item)
                current_dict = [item for item in current_dict if item[JsonBaseModelKeys.OBJECT_ID] != current_item[JsonBaseModelKeys.OBJECT_ID]]
                current_dict.append(current_item)
    else:
        if JsonBaseModelKeys.OBJECT_ID not in new_dict.keys():
            raise BackEndException(
                ErrorMessages.BAD_DATA,
                ErrorCodes.BAD_REQUEST)

        for key in new_dict.keys():
            if type(new_dict[key]) in (dict, list):
                current_dict[key] = merge_data(current_dict[key], new_dict[key])
            else:
                current_dict[key] = new_dict[key]
    return current_dict
