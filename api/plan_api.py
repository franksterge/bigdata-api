"""
: HTTP handlers for Plan related requests.
"""
import json
from flask import Blueprint, request, jsonify, Response
from constants.error_lib import ErrorCodes, ErrorMessages
from service import plan_service
from constants.json_constants import JsonPlanKeys

PLAN_API = Blueprint('student_profile_api', __name__)

@PLAN_API.route('', methods=['POST'])
def create_plan():
    new_plan_dict = request.get_json()
    new_plan_obj = plan_service.create_plan(new_plan_dict)
    return Response(status=ErrorCodes.OK, response=json.dumps(new_plan_obj.to_json()), mimetype='application/json')
