from flask import request, make_response
from apihelpers import check_endpoint_info, check_data_sent
import json
from dbhelpers import run_statement

def post():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    valid_token = run_statement('CALL token_check(?)', [request.headers.get('token')])

    if(type(valid_token) == list and valid_token[0]['client_id'] != 0):
        is_valid = check_endpoint_info(request.json, ['name'])
        if(is_valid != None):
            return make_response(json.dumps(is_valid,default=str), 400)
        
        results = run_statement('CALL add_college(?)', [request.json.get('name')])

        if(type(results) == list and results[0]['college_id'] != 0):
            return make_response(json.dumps(results[0], default=str), 200)
        elif(type(results) == list and results[0]['college_id'] == 0):
            return make_response(json.dumps(results[0], default=str), 400)
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)