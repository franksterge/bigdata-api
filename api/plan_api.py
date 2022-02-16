"""
: HTTP handlers for Plan related requests.
"""
import json
from flask import Blueprint, Response, request
from constants.error_lib import BackEndException, ErrorMessages, ErrorCodes
from service import plan_service
from util import validation
from util import etag_cache
from util.dynamo_util import DecimalEncoder
from werkzeug.datastructures import ETags


PLAN_API = Blueprint('student_profile_api', __name__)


@PLAN_API.route('', methods=['POST'])
@validation.validate_payload
def create_plan(payload):
    new_plan_dict = payload
    new_plan_obj = plan_service.create_plan(new_plan_dict)
    response = Response(status=ErrorCodes.OK, response=json.dumps(new_plan_obj.to_json()), mimetype='application/json')
    response.add_etag()
    etag_cache.append(response.get_etag()[0])
    return response

@PLAN_API.route('/<plan_id>', methods=['GET'])
def get_plan(plan_id):
    if request.if_none_match is not None:
        current_etags = request.if_none_match
        for etag in etag_cache:
            if current_etags.contains(etag):
                raise BackEndException(ErrorMessages.CONTENT_NOT_CHANGED, ErrorCodes.NOT_CHANGED)

    plan_obj = plan_service.get_plan(plan_id)
    response = Response(status=ErrorCodes.OK, response=json.dumps(plan_obj.to_json(), cls=DecimalEncoder), mimetype='application/json')
    response.add_etag()
    etag_cache.append(response.get_etag()[0])
    return response


@PLAN_API.route('/<plan_id>', methods=['DELETE'])
def delete_plan(plan_id):
    plan_service.delete_plan(plan_id)
    return Response(status=ErrorCodes.EMPTY_CONTENT)
