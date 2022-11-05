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
        is_valid = check_endpoint_info(request.json, ['student_id', 'applied', 'applied_at', 'approved', 'analyst'])
        if(is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)

        results = run_statement('CALL add_visa(?,?,?,?,?)', [request.json.get('student_id'), request.json.get('applied'), request.json.get('applied_at'), request.json.get('approved'), request.json.get('analyst')])

        if(type(results) == list and len(results) != 0):
            return make_response(json.dumps(results, default=str), 200)
        elif(type(results) == list and len(results) == 0):
            return make_response(json.dumps(results[0], default=str), 400)
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)

    else:
        return make_response(json.dumps("Wrong token", default=str), 400)

def get():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    valid_token = is_valid_token(request.headers.get('token'))

    if(valid_token):
        results = run_statement('CALL get_all_visa()')

        if(type(results) == list and len(results) != 0):
            return make_response(json.dumps(results, default=str), 200)
        elif(type(results) == list and len(results) == 0):
            return make_response(json.dumps(results, default=str), 400)
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)
    else:
        return make_response(json.dumps("Wrong token", default=str), 400)
