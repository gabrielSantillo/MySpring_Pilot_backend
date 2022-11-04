from flask import request, make_response
from apihelpers import check_endpoint_info, check_data_sent, is_valid_token
import json
from dbhelpers import run_statement

def post():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    valid_token = is_valid_token(request.headers.get('token'))

    if(valid_token):
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

def get():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    valid_token = is_valid_token(request.headers.get('token'))

    if(valid_token):
        results = run_statement('CALL get_all_colleges()')

        if(type(results) == list):
            return make_response(json.dumps(results, default=str), 200)
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)

def patch():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    valid_token = is_valid_token(request.headers.get('token'))

    if(valid_token):
        is_valid = check_endpoint_info(request.json, ['id', 'name'])
        if(is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)

        results = run_statement('CALL edit_college(?,?)', [request.json.get('id'), request.json.get('name')])

        if(type(results) == list and results[0]['row_updated'] == 1):
            return make_response(json.dumps(results[0], default=str), 200)
        elif(type(results) == list and results[0]['row_updated'] == 0):
            return make_response(json.dumps(results[0], default=str), 400)
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)

