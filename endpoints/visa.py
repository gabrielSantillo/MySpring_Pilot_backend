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
        is_valid = check_endpoint_info(request.json, ['student_id', 'applied', 'applied_at', 'approved', 'analyst'])
        if(is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)

        results = run_statement('CALL add_visa(?,?,?,?,?)', [request.json.get('student_id'), request.json.get('applied'), request.json.get('applied_at'), request.json.get('approved'), request.json.get('analyst')])

        if(type(results) == list and len(results) != 0):
            return make_response(json.dumps(results[0], default=str), 200)
        elif(type(results) == list and len(results) == 0):
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
        results = run_statement('CALL get_all_visa()')

        if(type(results) == list and len(results) != 0):
            return make_response(json.dumps(results, default=str), 200)
        elif(type(results) == list and len(results) == 0):
            return make_response(json.dumps(results, default=str), 400)
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
        is_valid = check_endpoint_info(request.json, ['visa_id'])
        if(is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)

        visa_info = run_statement('CALL get_visa_by_id(?)', [request.json.get('visa_id')])

        if(type(visa_info) == list and len(visa_info) != 0):
            update_visa_info = check_data_sent(request.json, visa_info[0], ['visa_id', 'student_id', 'applied', 'applied_at', 'approved', 'analyst'])

            results = run_statement('CALL edit_visa(?,?,?,?,?,?)', [update_visa_info['visa_id'], update_visa_info['student_id'], update_visa_info['applied'], update_visa_info['applied_at'], update_visa_info['approved'], update_visa_info['analyst']])

            if(type(results) == list and results[0]['row_updated'] == 1):
                return make_response(json.dumps(results[0], default=str), 200)
            elif(type(results) == list and results[0]['row_updated'] == 0):
                return make_response(json.dumps(results[0], default=str), 400)
            else:
                return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)
        
        else:
            return make_response(json.dumps("Wrong visa_id", default=str), 400)

    elif(valid_token == "invalid"):
        return make_response(json.dumps("TOKEN EXPIRED", default=str), 403)
    elif(len(valid_token) == 0):
        return make_response(json.dumps("WRONG TOKEN", default=str), 400)
    else:
        return make_response(json.dumps(valid_token, default=str), 500)
