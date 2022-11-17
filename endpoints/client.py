from uuid import uuid4
from flask import request, make_response
from apihelpers import check_endpoint_info, check_data_sent, token_validation
import secrets
import json
from dbhelpers import run_statement

# this is the POST function that is responsible to post new client
def post():
    # verifying if some value was sent as header
    is_valid = check_endpoint_info(request.json, ['first_name', 'last_name', 'email', 'password'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    # creating a token by using the built in function secrets
    token = secrets.token_hex(nbytes=None)
    # creating a salt by using the built in function uuid4 to be sent and hash the password in the db
    salt = uuid4().hex

    # calling the function that will add a client
    results = run_statement('CALL add_client(?,?,?,?,?,?)', [request.json.get('first_name'), request.json.get('last_name'), request.json.get('email'), request.json.get('password'), token, salt])

    # if the response is a list and the length is different than zero send 200 as response
    if(type(results) == list and len(results) != 0):
        return make_response(json.dumps(results[0], default=str), 200)
    # else a 500 as response
    else:
        return make_response(json.dumps(results[0], default=str), 500)

# this is the GET function that is responsible to get all clients
def get():

    # calling the function that will verify if this token is valid
    valid_token = token_validation(request.headers.get('token'))
    if(valid_token == "valid"):
        # calling the procedure that will get all clients
        results = run_statement('CALL get_client()')

        # if the response is a list and the length is different than zero send 200 as response
        if(type(results) == list and len(results) != 0):
            return make_response(json.dumps(results), 200)
        # if the response is a list and the length is equal than zero
        elif(type(results) == list and len(results) == 0):
            return make_response(json.dumps("There is no user in the system.", default=str), 400)
        else:
            return make_response(json.dumps("Sorry, an error has occurred"), 500)
    # if the response send back while checking the token is "invalid" send a 403 as response
    elif(valid_token == "invalid"):
        return make_response(json.dumps("TOKEN EXPIRED", default=str), 403)
    # if the response send back while checking the token is "invalid" send a 403 as response
    elif(len(valid_token) == 0):
        return make_response(json.dumps("WRONG TOKEN", default=str), 400)
    else:
        return make_response(json.dumps(valid_token, default=str), 500)

# this is the PATCH function that is responsible to update a client based on its id
def patch():
    # verifying if some value was sent as header
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if(is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    # calling the function that will verify if this token is valid
    valid_token = token_validation(request.headers.get('token'))
    if(valid_token == "valid"):
        # in case the response from the function is "valid" will keep going with the processes of patching a client
        # getting the client info basesd on its token
        user_info = run_statement('CALL get_client_by_token(?)', [request.headers.get('token')])
        # verifying if the response is different than a list and its length is different than 1 to send a 400 as response
        if(type(user_info) != list or len(user_info) != 1):
            return make_response(json.dumps(user_info, default=str), 400)

        # updating the user info with the data sent to be updated
        update_user_info = check_data_sent(request.json, user_info[0], ['first_name', 'last_name', 'email', 'password'])

        # calling the function that will update the user info
        results = run_statement('CALL edit_client(?,?,?,?,?)', [update_user_info['first_name'], update_user_info['last_name'], update_user_info['email'], update_user_info['password'], request.headers.get('token')])

        # if the response is a lsit and at row_updateded is equal to 1, send 200 as response
        if(type(results) == list and results[0]['row_updated'] == 1):
            return make_response(json.dumps(results[0], default=str), 200)
         # if the response is a lsit and at row_updateded is equal to 0, send 400 as response
        elif(type(results) == list and results[0]['row_updated'] == 0):
            return make_response(json.dumps(results[0], default=str), 400)
        # else send an 500 as internal error
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)
    # if the response from the validation function is "invalid" means that the token expired
    elif(valid_token == "invalid"):
        return make_response(json.dumps("TOKEN EXPIRED", default=str), 403)
    # if the response from the validation function is 0 means that the token is invalid
    elif(len(valid_token) == 0):
        return make_response(json.dumps("WRONG TOKEN", default=str), 400)
    else:
        return make_response(json.dumps(valid_token, default=str), 500)