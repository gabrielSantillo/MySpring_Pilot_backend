from flask import request, make_response
from apihelpers import check_endpoint_info, is_valid_token, check_data_sent
import json
from dbhelpers import run_statement

def post():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    valid_token = is_valid_token(request.headers.get('token'))

    if(valid_token):
        is_valid = check_endpoint_info(request.form, ['description'])
        if(is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)
    else:
        return make_response(json.dumps("Wrong token", default=str), 400)
