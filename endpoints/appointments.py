from flask import request, make_response
from apihelpers import check_endpoint_info, check_data_sent, token_validation
import json
from dbhelpers import run_statement

def post():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    valid_token = token_validation(request.headers.get('token'))
    if(valid_token == "valid"): 
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
    elif(valid_token == "invalid"):
        return make_response(json.dumps("TOKEN EXPIRED", default=str), 403)
    elif(len(valid_token) == 0):
        return make_response(json.dumps("WRONG TOKEN", default=str), 400)
    else:
        return make_response(json.dumps(valid_token, default=str), 500)

def get():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    valid_token = run_statement('CALL token_check(?)', [request.headers.get('token')])

    if(type(valid_token) == list and len(valid_token) == 1):
        results = run_statement('CALL get_all_appointments()')

        if(type(results) == list):
            return make_response(json.dumps(results, default=str), 200)
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)
    else:
        return make_response(json.dumps("Wrong token", default=str), 400)

def patch():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    valid_token = run_statement('CALL token_check(?)', [request.headers.get('token')])

    if(type(valid_token) == list and valid_token[0]['client_id'] != 0):
        is_valid = check_endpoint_info(request.json, ['appointment_id'])
        if(is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)
        
        appointment_info = run_statement('CALL get_appointment_by_id(?)', [request.json.get('appointment_id')])

        update_appointment_info = check_data_sent(request.json, appointment_info[0], ['client_id', 'first_name', 'last_name', 'email', 'contract_signed', 'appointment_date'])

        results = run_statement('CALL edit_appointment(?,?,?,?,?,?,?)', [update_appointment_info['client_id'], update_appointment_info['first_name'], update_appointment_info['last_name'], update_appointment_info['email'], update_appointment_info['contract_signed'], update_appointment_info['appointment_date'], request.json.get('appointment_id')])

        if(type(results) == list and results[0]['row_updated'] == 1):
            return make_response(json.dumps(results[0], default=str), 200)
        elif(type(results) == list and results[0]['row_updated'] == 0):
            return make_response(json.dumps(results[0], default=str), 400)
        else:
            return make_response(json.dumps("Sorry, an error has ocurred", default=str), 500)

    else:
        make_response(json.dumps("Wrong token.", default=str), 400)

