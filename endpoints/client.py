from uuid import uuid4
from flask import request, make_response
from apihelpers import check_endpoint_info, check_data_sent, token_validation
import secrets
import json
from dbhelpers import run_statement

def post():
    is_valid = check_endpoint_info(request.json, ['first_name', 'last_name', 'email', 'password'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    token = secrets.token_hex(nbytes=None)
    salt = uuid4().hex

    results = run_statement('CALL add_client(?,?,?,?,?,?)', [request.json.get('first_name'), request.json.get('last_name'), request.json.get('email'), request.json.get('password'), token, salt])

    if(type(results) == list and len(results) != 0):
        return make_response(json.dumps(results[0], default=str), 200)
    else:
        return make_response(json.dumps(results[0], default=str), 500)

def get():
    results = run_statement('CALL get_client()')

    if(type(results) == list and len(results) != 0):
        return make_response(json.dumps(results), 200)
    elif(type(results) == list and len(results) == 0):
        return make_response(json.dumps("There is no user in the system.", default=str), 400)
    else:
        return make_response(json.dumps("Sorry, an error has occurred"), 500)

def patch():
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    valid_token = token_validation(request.headers.get('token'))
    if(valid_token == None):
        return make_response(json.dumps("WRONG TOKEN", default=str), 400)
    elif(valid_token):
        user_info = run_statement('CALL get_client_by_token(?)', [request.headers.get('token')])
        if(type(user_info) != list or len(user_info) != 1):
            return make_response(json.dumps(user_info, default=str), 400)

        update_user_info = check_data_sent(request.json, user_info[0], ['first_name', 'last_name', 'email', 'password'])

        results = run_statement('CALL edit_client(?,?,?,?,?)', [update_user_info['first_name'], update_user_info['last_name'], update_user_info['email'], update_user_info['password'], request.headers.get('token')])

        if(type(results) == list and results[0]['row_updated'] == 1):
            return make_response(json.dumps(results[0], default=str), 200)
        elif(type(results) == list and results[0]['row_updated'] == 0):
            return make_response(json.dumps(results[0], default=str), 400)
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)
    else:
        return make_response(json.dumps("TOKEN EXPIRED", default=str), 200)