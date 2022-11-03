from uuid import uuid4
from flask import request, make_response
from apihelpers import check_endpoint_info, check_data_sent
import secrets
import json
from dbhelpers import run_statement

def post():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    is_valid = check_endpoint_info(request.json, ['first_name', 'last_name', 'email', 'date'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid,default=str), 400)

    results = run_statement('CALL add_appointment(?,?,?,?,?)', [request.json.get('first_name'), request.json.get('last_name'), request.json.get('email'), request.json.get('date'), request.headers.get('token')])

    if(type(results) == list and results[0]["appointment_id"] != 0):
        return make_response(json.dumps(results[0],default=str), 200)
    elif(type(results) == list and results[0]["appointment_id"] == 0):
        return make_response(json.dumps("Wrong token", default=str), 400)
    else:
        return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)

def get():
    results = run_statement('CALL get_all_appointments()')

    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)