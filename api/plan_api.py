"""
: HTTP handlers for Plan related requests.
"""
import json
from flask import Blueprint, Response, request
from constants.error_lib import BackEndException, ErrorMessages, ErrorCodes
from service import plan_service
from util import validation, etag_cache, authorization
from util.dynamo_util import DecimalEncoder
from util.elasticsearch_util import es_connection


PLAN_API = Blueprint('student_profile_api', __name__)


@PLAN_API.route('', methods=['POST'])
@authorization.verify_user
@validation.validate_payload
def create_plan(payload):
    if request.if_match is not None:
        current_etags = request.if_match
        for etag in etag_cache:
            if current_etags.contains(etag):
                raise BackEndException(ErrorMessages.CONTENT_NOT_CHANGED, ErrorCodes.PRECONDITION_FAILED)

    new_plan_dict = payload
    new_plan_obj = plan_service.create_plan(new_plan_dict)

    response = Response(status=ErrorCodes.OK, response=json.dumps(new_plan_obj.to_dict()), mimetype='application/json')
    response.add_etag()
    etag_cache.append(response.get_etag()[0])
    return response

@PLAN_API.route('/<plan_id>', methods=['GET'])
@authorization.verify_user
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
@authorization.verify_user
def delete_plan(plan_id):
    plan_service.delete_plan(plan_id)
    return Response(status=ErrorCodes.EMPTY_CONTENT)

@PLAN_API.route('/<plan_id>', methods=['PATCH'])
@authorization.verify_user
def patch_plan(plan_id):
    if request.if_match is not None:
        current_etags = request.if_match
        for etag in etag_cache:
            if current_etags.contains(etag):
                raise BackEndException(ErrorMessages.CONTENT_NOT_CHANGED, ErrorCodes.PRECONDITION_FAILED)
    new_plan_dict = request.get_json()
    plan_obj = plan_service.patch_plan(plan_id, new_plan_dict)
    response = Response(status=ErrorCodes.OK, response=json.dumps(plan_obj.to_json(), cls=DecimalEncoder), mimetype='application/json')
    response.add_etag()
    etag_cache.append(response.get_etag()[0])
    return response
