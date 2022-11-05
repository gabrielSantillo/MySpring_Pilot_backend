from flask import request, make_response
from apihelpers import check_endpoint_info, is_valid_token
import json
from dbhelpers import run_statement

def post():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    valid_token = is_valid_token(request.headers.get('token'))

    if(valid_token):
        is_valid = check_endpoint_info(request.json, ['student_id', 'applied', 'date_applied', 'loa_process'])
        if(is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)
        
        results = run_statement('CALL add_application_status(?,?,?,?)', [request.json.get('student_id'), request.json.get('applied'), request.json.get('date_applied'), request.json.get('loa_process')])

        if(type(results) == list and results[0]['application_id'] != 0):
            return make_response(json.dumps(results[0], default=str), 200)
        elif(type(results) == list and results[0]['application_id'] == 0):
            return make_response(json.dumps(results[0], default=str), 400)
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)

def get():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    valid_token = is_valid_token(request.headers.get('token'))

    if(valid_token):
        results = run_statement('CALL get_all_application_status()')

        if(type(results) == list and len(results) != 0):
            return make_response(json.dumps(results, default=str), 200)
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)