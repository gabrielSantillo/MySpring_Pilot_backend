from flask import request, make_response
from apihelpers import check_endpoint_info, check_data_sent, token_validation
import json
from dbhelpers import run_statement

# this is the POST function that is responsible to post new application status


def post():
    # verifying if some value was sent as header
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if (is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    # calling the function that will verify if this token is valid
    valid_token = token_validation(request.headers.get('token'))
    if (valid_token == "valid"):

        # in case the response from the function is "valid" will keep going with the processes of adding an aplication status by calling a fuction that will verify if the user sent the correct key values
        is_valid = check_endpoint_info(
            request.json, ['student_id', 'applied', 'date_applied', 'loa_process'])
        if (is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)

        # adding a new application status
        results = run_statement('CALL add_application_status(?,?,?,?)', [request.json.get(
            'student_id'), request.json.get('applied'), request.json.get('date_applied'), request.json.get('loa_process')])

        # if results is a list and at 0 at 'application_id" is different than zero, send back a 200 response. If it is equal to zero, send back the response showing that none row was updated and else, send back that an internal error has occurred
        if (type(results) == list and results[0]['application_id'] != 0):
            return make_response(json.dumps(results[0], default=str), 200)
        elif (type(results) == list and results[0]['application_id'] == 0):
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


# this is the GET function that is responsible to get all application status
def get():
    # verifying if some value was sent as header
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if (is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    # calling the function that will verify if this token is valid
    valid_token = token_validation(request.headers.get('token'))
    if (valid_token == "valid"):
        # in case the response from the function is "valid" will keep going with the processes of getting aplication status
        results = run_statement('CALL get_all_application_status()')

        # if results is a list and his length is different than zero return 200
        if (type(results) == list and len(results) != 0):
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


# this is the PATCH function that is responsible to update an application status based on its id
def patch():
    # verifying if some value was sent as header
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if (is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    # calling the function that will verify if this token is valid
    valid_token = token_validation(request.headers.get('token'))
    if (valid_token == "valid"):
        # in case the response from the function is "valid" will keep going with the processes of patching aplication status
        is_valid = check_endpoint_info(request.json, ['application_status_id'])
        if (is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)

        # getting the applicantion status by id
        application_status_info = run_statement('CALL get_application_status_by_id(?)', [
                                                request.json.get('application_status_id')])

        # checking to see if the response is valid to continue with the patching process
        if (type(application_status_info) == list and len(application_status_info) != 0):
            # calling a function that will send back the entire object with what was not updated and what was
            update_application_status = check_data_sent(request.json, application_status_info[0], [
                                                        'application_status_id', 'student_id', 'applied', 'date_applied', 'loa_process'])

            # adding this update in the database
            results = run_statement('CALL edit_application_status(?,?,?,?,?)', [update_application_status['application_status_id'], update_application_status[
                                    'student_id'],  update_application_status['applied'],  update_application_status['date_applied'],  update_application_status['loa_process']])

            # if the response is a list and at row_updated is 1, send a 200 as response
            if (type(results) == list and results[0]['row_updated'] == 1):
                return make_response(json.dumps(results[0], default=str), 200)
            # if the response is a list and at row_updated is 0, send a 400 as response
            elif (type(results) == list and results[0]['row_updated'] == 0):
                return make_response(json.dumps(results[0], default=str), 400)
            # else send 500 as an internal error
            else:
                return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)

        # if the length of application_status_info is not different than zero, send a 400 as response
        else:
            return make_response(json.dumps("Wrong application_status_id", default=str), 400)
    # if the response send back while checking the token is "invalid" send a 403 as response
    elif (valid_token == "invalid"):
        return make_response(json.dumps("TOKEN EXPIRED", default=str), 403)
    # if the response send back while checking the token is "invalid" send a 403 as response
    elif (len(valid_token) == 0):
        return make_response(json.dumps("WRONG TOKEN", default=str), 400)
    else:
        return make_response(json.dumps(valid_token, default=str), 500)
