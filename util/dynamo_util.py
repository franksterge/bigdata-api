import json
from decimal import Decimal
from constants.constants import DynamoKeys

def query_dynamo_db(table, partition_key, search_key=None, filter_condition=None):
    """
    Queries dynamo db with given partition key condition.
    :param table: Dynamo table
    :param partition_key: pkey condition expression
    :param search_key: skey condition expression
    :param filter_condition: additional filter expression
    :return: a list of dictionaries containing the query results.
    """
    query_condition = partition_key
    if search_key:
        query_condition &= search_key
    if filter_condition:
        response = table.query(
            KeyConditionExpression=query_condition,
            FilterExpression=filter_condition)
    else:
        response = table.query(
            KeyConditionExpression=query_condition
        )
    return response[DynamoKeys.BATCH_CONTENTS]


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
