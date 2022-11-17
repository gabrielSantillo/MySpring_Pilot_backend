from flask import request, make_response
from apihelpers import check_endpoint_info, check_data_sent, token_validation
import json
from dbhelpers import run_statement

# this is the POST function that is responsible to post new visa


def post():
    # verifying if some value was sent as header
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if (is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    # calling the function that will verify if this token is valid
    valid_token = token_validation(request.headers.get('token'))
    if (valid_token == "valid"):
        # in case the response from the function is "valid" will keep going with the processes of adding a visa by calling a fuction that will verify if the user sent the correct key values
        is_valid = check_endpoint_info(
            request.json, ['student_id', 'applied', 'applied_at', 'approved', 'analyst'])
        if (is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)

        # adding a new visa
        results = run_statement('CALL add_visa(?,?,?,?,?)', [request.json.get('student_id'), request.json.get(
            'applied'), request.json.get('applied_at'), request.json.get('approved'), request.json.get('analyst')])

        # if results is a list and the length is different than zero, send back a 200 response. If it is equal to zero, send back the response showing that none row was updated and else, send back that an internal error has occurred
        if (type(results) == list and len(results) != 0):
            return make_response(json.dumps(results[0], default=str), 200)
        elif (type(results) == list and len(results) == 0):
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


# this is the GET function that is responsible to get all visas
def get():
    # verifying if some value was sent as header
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if (is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    # calling the function that will verify if this token is valid
    valid_token = token_validation(request.headers.get('token'))
    if (valid_token == "valid"):
        # in case the response from the function is "valid" will keep going with the processes of getting visas
        results = run_statement('CALL get_all_visa()')

        # if results is a list and his length is different than zero return 200
        if (type(results) == list and len(results) != 0):
            return make_response(json.dumps(results, default=str), 200)
        # if results is a list and his length is equal than zero return 400
        elif (type(results) == list and len(results) == 0):
            return make_response(json.dumps(results, default=str), 400)
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

# this is the PATCH function that is responsible to update a visa based on its id


def patch():
    # verifying if some value was sent as header
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if (is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    # calling the function that will verify if this token is valid
    valid_token = token_validation(request.headers.get('token'))
    if (valid_token == "valid"):
        # in case the response from the function is "valid" will keep going with the processes of patching visa
        is_valid = check_endpoint_info(request.json, ['visa_id'])
        if (is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)

        # getting the appointment by id
        visa_info = run_statement('CALL get_visa_by_id(?)', [
                                  request.json.get('visa_id')])

        # checking to see if the response is valid to continue with the patching process
        if (type(visa_info) == list and len(visa_info) != 0):
            update_visa_info = check_data_sent(request.json, visa_info[0], [
                                               'visa_id', 'student_id', 'applied', 'applied_at', 'approved', 'analyst'])

            # calling the function that will edit a visa
            results = run_statement('CALL edit_visa(?,?,?,?,?,?)', [update_visa_info['visa_id'], update_visa_info['student_id'],
                                    update_visa_info['applied'], update_visa_info['applied_at'], update_visa_info['approved'], update_visa_info['analyst']])

            # if the response is a list and the row_updated is equal than 1 send 200 as response
            if (type(results) == list and results[0]['row_updated'] == 1):
                return make_response(json.dumps(results[0], default=str), 200)
            # if the response is a list and the row_updated is equal than 0 send 400 as response
            elif (type(results) == list and results[0]['row_updated'] == 0):
                return make_response(json.dumps(results[0], default=str), 400)
            # else send 500 as an internal error
            else:
                return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)

        else:
            return make_response(json.dumps("Wrong visa_id", default=str), 400)

    # if the response from the validation function is "invalid" means that the token expired
    elif (valid_token == "invalid"):
        return make_response(json.dumps("TOKEN EXPIRED", default=str), 403)
    # if the response from the validation function is 0 means that the token is invalid
    elif (len(valid_token) == 0):
        return make_response(json.dumps("WRONG TOKEN", default=str), 400)
    else:
        return make_response(json.dumps(valid_token, default=str), 500)
