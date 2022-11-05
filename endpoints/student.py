from flask import request, make_response
from apihelpers import check_endpoint_info, check_data_sent, is_valid_token
import json
from dbhelpers import run_statement

def post():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    is_valid = check_endpoint_info(request.json, ['appointment_id', 'college_id', 'english', 'app_form', 'comission'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    results = run_statement('CALL add_student(?,?,?,?,?,?)', [request.json.get('appointment_id'), request.json.get('college_id'), request.json.get('english'), request.json.get('app_form'), request.json.get('comission'), request.headers.get('token')])

    if(type(results) == list and results[0]['student_id'] != 0):
        return make_response(json.dumps(results[0], default=str), 200)
    elif(type(results) == list and results[0]['student_id'] == 0):
        return make_response(json.dumps("Wrong token", default=str), 400)
    else:
        return make_response(json.dumps("Sorry, an error has occurred.", default=str), 500)

def get():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    results = run_statement('CALL get_all_students(?)', [request.headers.get('token')])

    if(type(results) == list and len(results) != 0):
        return make_response(json.dumps(results, default=str), 200)
    elif(type(results) == list and len(results) == 0):
        return make_response(json.dumps("Wrong token", default=str), 400)
    else:
        return make_response(json.dumps("Sorry, an error has occurred.", default=str), 500)
