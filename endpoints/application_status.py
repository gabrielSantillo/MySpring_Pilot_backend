from flask import request, make_response
from apihelpers import check_endpoint_info, is_valid_token, check_data_sent, token_validation
import json
from dbhelpers import run_statement

def post():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    valid_token = token_validation(request.headers.get('token'))
    if(valid_token == "valid"):
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

    valid_token = token_validation(request.headers.get('token'))
    if(valid_token == "valid"):
        results = run_statement('CALL get_all_application_status()')

        if(type(results) == list and len(results) != 0):
            return make_response(json.dumps(results, default=str), 200)
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)
    elif(valid_token == "invalid"):
        return make_response(json.dumps("TOKEN EXPIRED", default=str), 403)
    elif(len(valid_token) == 0):
        return make_response(json.dumps("WRONG TOKEN", default=str), 400)
    else:
        return make_response(json.dumps(valid_token, default=str), 500)

def patch():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    valid_token = token_validation(request.headers.get('token'))
    if(valid_token == "valid"):
        is_valid = check_endpoint_info(request.json, ['application_status_id'])
        if(is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)
            
        application_status_info = run_statement('CALL get_application_status_by_id(?)', [request.json.get('application_status_id')])

        if(type(application_status_info) == list and len(application_status_info) != 0):
            update_application_status = check_data_sent(request.json, application_status_info[0], ['application_status_id', 'student_id', 'applied', 'date_applied', 'loa_process'])

            results = run_statement('CALL edit_application_status(?,?,?,?,?)', [update_application_status['application_status_id'], update_application_status['student_id'],  update_application_status['applied'],  update_application_status['date_applied'],  update_application_status['loa_process']])

            if(type(results) == list and results[0]['row_updated'] == 1):
                return make_response(json.dumps(results[0], default=str), 200)
            elif(type(results) == list and results[0]['row_updated'] == 0):
                return make_response(json.dumps(results[0], default=str), 400)
            else:
                return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)

        else:
            return make_response(json.dumps("Wrong application_status_id", default=str), 400)
    elif(valid_token == "invalid"):
        return make_response(json.dumps("TOKEN EXPIRED", default=str), 403)
    elif(len(valid_token) == 0):
        return make_response(json.dumps("WRONG TOKEN", default=str), 400)
    else:
        return make_response(json.dumps(valid_token, default=str), 500)