from flask import request, make_response
from apihelpers import check_endpoint_info, token_validation, is_valid_token
import json
from dbhelpers import run_statement

# this is the POST function that is responsible to post new college


def post():
    # verifying if some value was sent as header
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if (is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    # calling the function that will verify if this token is valid
    valid_token = token_validation(request.headers.get('token'))
    if (valid_token == "valid"):
        # in case the response from the function is "valid" will keep going with the processes of adding an appointment by calling a fuction that will verify if the user sent the correct key values
        is_valid = check_endpoint_info(request.json, ['name'])
        if (is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)

        # adding a new college
        results = run_statement('CALL add_college(?)', [
                                request.json.get('name')])

        # if results is a list and at 0 at 'appointment_id" is different than zero, send back a 200 response. If it is equal to zero, send back the response showing that none row was updated and else, send back that an internal error has occurred
        if (type(results) == list and results[0]['college_id'] != 0):
            return make_response(json.dumps(results[0], default=str), 200)
        elif (type(results) == list and results[0]['college_id'] == 0):
            return make_response(json.dumps(results[0], default=str), 400)
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)

    # if the response from the validation function is "invalid" means that the token expired
    elif (valid_token == "invalid"):
        return make_response(json.dumps("TOKEN EXPIRED", default=str), 403)
    # if the response from the validation function is 0 means that the token is invalid
    elif (len(valid_token) == 0):
        return make_response(json.dumps("WRONG TOKEN", default=str), 400)
    else:
        return make_response(json.dumps(valid_token, default=str), 500)

# this is the GET function that is responsible to get all colleges


def get():
    # verifying if some value was sent as header
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if (is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    # calling the function that will verify if this token is valid
    valid_token = token_validation(request.headers.get('token'))
    if (valid_token == "valid"):
        # in case the response from the function is "valid" will keep going with the processes of getting colleges
        results = run_statement('CALL get_all_colleges()')

        # if results is a list and his length is different than zero return 200
        if (type(results) == list):
            return make_response(json.dumps(results, default=str), 200)
        # else return 500, internal error
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)

    # if the response from the validation function is "invalid" means that the token expired
    elif (valid_token == "invalid"):
        return make_response(json.dumps("TOKEN EXPIRED", default=str), 403)
    # if the response from the validation function is 0 means that the token is invalid
    elif (len(valid_token) == 0):
        return make_response(json.dumps("WRONG TOKEN", default=str), 400)
    else:
        return make_response(json.dumps(valid_token, default=str), 500)

# this is the PATCH function that is responsible to update a college based on its id


def patch():
    # verifying if some value was sent as header
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if (is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    # calling the function that will verify if this token is valid
    valid_token = token_validation(request.headers.get('token'))
    # checking to see if the response is valid to continue with the patching process
    if (valid_token == "valid"):
        # in case the response from the function is "valid" will keep going with the processes of patching college
        is_valid = check_endpoint_info(request.json, ['id', 'name'])
        if (is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)

        # calling the function that will edit a college
        results = run_statement('CALL edit_college(?,?)', [
                                request.json.get('id'), request.json.get('name')])

        # if the response is a list and the row_updated is equal than 1 send 200 as response
        if (type(results) == list and results[0]['row_updated'] == 1):
            return make_response(json.dumps(results[0], default=str), 200)
        # if the response is a list and the row_updated is equal than 0 send 400 as response
        elif (type(results) == list and results[0]['row_updated'] == 0):
            return make_response(json.dumps(results[0], default=str), 400)
        # else send 500 as an internal error
        else:
            return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)
    # if the response from the validation function is "invalid" means that the token expired
    elif (valid_token == "invalid"):
        return make_response(json.dumps("TOKEN EXPIRED", default=str), 403)
    # if the response from the validation function is 0 means that the token is invalid
    elif (len(valid_token) == 0):
        return make_response(json.dumps("WRONG TOKEN", default=str), 400)
    else:
        return make_response(json.dumps(valid_token, default=str), 500)
