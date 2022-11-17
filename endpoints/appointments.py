from flask import request, make_response
from apihelpers import check_endpoint_info, check_data_sent, token_validation
import json
from dbhelpers import run_statement

# this is the POST function that is responsible to post new appointment


def post():
    # verifying if some value was sent as header
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if (is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    # calling the function that will verify if this token is valid
    valid_token = token_validation(request.headers.get('token'))
    if (valid_token == "valid"):

        # in case the response from the function is "valid" will keep going with the processes of adding an appointment by calling a fuction that will verify if the user sent the correct key values
        is_valid = check_endpoint_info(
            request.json, ['first_name', 'last_name', 'email', 'date'])
        if (is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)

        # adding a new appointment
        results = run_statement('CALL add_appointment(?,?,?,?,?)', [request.json.get('first_name'), request.json.get(
            'last_name'), request.json.get('email'), request.json.get('date'), request.headers.get('token')])

        # if results is a list and at 0 at 'appointment_id" is different than zero, send back a 200 response. If it is equal to zero, send back the response showing that none row was updated and else, send back that an internal error has occurred
        if (type(results) == list and results[0]["appointment_id"] != 0):
            return make_response(json.dumps(results[0], default=str), 200)
        elif (type(results) == list and results[0]["appointment_id"] == 0):
            return make_response(json.dumps("Wrong token", default=str), 400)
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

# this is the GET function that is responsible to get all appointments


def get():
    # verifying if some value was sent as header
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if (is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    # calling the function that will verify if this token is valid
    valid_token = token_validation(request.headers.get('token'))
    if (valid_token == "valid"):
        # in case the response from the function is "valid" will keep going with the processes of getting appointments
        results = run_statement('CALL get_all_appointments()')

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

# this is the PATCH function that is responsible to update an appointment based on its id


def patch():
    # verifying if some value was sent as header
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if (is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    # calling the function that will verify if this token is valid
    valid_token = token_validation(request.headers.get('token'))
    if (valid_token == "valid"):
        # in case the response from the function is "valid" will keep going with the processes of patching appointment
        is_valid = check_endpoint_info(request.json, ['appointment_id'])
        if (is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)

        # getting the appointment by id
        appointment_info = run_statement('CALL get_appointment_by_id(?)', [
                                         request.json.get('appointment_id')])

        # checking to see if the response is valid to continue with the patching process
        if (type(appointment_info) == list and len(appointment_info) != 0):
            update_appointment_info = check_data_sent(request.json, appointment_info[0], [
                                                      'client_id', 'first_name', 'last_name', 'email', 'contract_signed', 'appointment_date'])

            # calling the function that will edit an appointment
            results = run_statement('CALL edit_appointment(?,?,?,?,?,?,?)', [update_appointment_info['client_id'], update_appointment_info['first_name'], update_appointment_info[
                                    'last_name'], update_appointment_info['email'], update_appointment_info['contract_signed'], update_appointment_info['appointment_date'], request.json.get('appointment_id')])

            # if the response is a list and the row_updated is equal than 1 send 200 as response
            if (type(results) == list and results[0]['row_updated'] == 1):
                return make_response(json.dumps(results[0], default=str), 200)
            # if the response is a list and the row_updated is equal than 0 send 400 as response
            elif (type(results) == list and results[0]['row_updated'] == 0):
                return make_response(json.dumps(results[0], default=str), 400)
            # else send 500 as an internal error
            else:
                return make_response(json.dumps("Sorry, an error has ocurred", default=str), 500)

        # if the length of appointment_info is not different than zero, send a 400 as response
        else:
            return make_response(json.dumps("Wrong appointment_id", default=str), 400)
    # if the response from the validation function is "invalid" means that the token expired
    elif (valid_token == "invalid"):
        return make_response(json.dumps("TOKEN EXPIRED", default=str), 403)
    # if the response from the validation function is 0 means that the token is invalid
    elif (len(valid_token) == 0):
        return make_response(json.dumps("WRONG TOKEN", default=str), 400)
    else:
        return make_response(json.dumps(valid_token, default=str), 500)
