from flask import request, make_response
from apihelpers import check_endpoint_info, check_data_sent
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

def patch():
    #is_valid_header = check_endpoint_info(request.headers, ['token'])
    #if(is_valid_header != None):
    #   return make_response(json.dumps(is_valid_header, default=str), 400)

    is_valid = check_endpoint_info(request.json, ['appointment_id'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)
    
    appointment_info = run_statement('CALL get_appointment_by_user_token(?)', [request.json.get('appointment_id')])

    update_appointment_info = check_data_sent(request.json, appointment_info[0], ['user_id', 'first_name', 'last_name', 'email', 'contract_signed', 'appointment_date'])

    results = run_statement('CALL edit_appointment(?,?,?,?,?,?,?)', [update_appointment_info['user_id'], update_appointment_info['first_name'], update_appointment_info['last_name'], update_appointment_info['email'], update_appointment_info['contract_signed'], update_appointment_info['appointment_date']])

